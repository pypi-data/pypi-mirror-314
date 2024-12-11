"""
TBD
"""
import asyncio
import json
import logging
import os
import ssl
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import requests
from urllib3.util import Url, parse_url
from urllib3.util.retry import Retry
from websockets import ConnectionClosed as WsConnectionClosed
from websockets.asyncio.client import connect as ws_connect

from .retry import retry

SSL_KWARGS = [
    'check_hostname',
    'hostname_checks_common_name',
    'verify_mode',
    'verify_flags',
    'options',
]

RETRY_KWARGS = [
    'tries',
    'delay',
    'backoff',
    'max_delay',
    'exceptions',
]

OWN_KWARGS = [
    'acquire_wait_for_timeout',
    'acquire_modulo',
    'disable_websocket',
    'raise_when_acquire_fails',
    'ws_ping_interval',
    'ws_ping_timeout',
    'ws_wait_for_timeout',
]
OWN_KWARGS.extend(RETRY_KWARGS)

logger = logging.getLogger(__name__)


class RelukkoDoRetry(Exception):
    """
    Exception thrown on some errors which we still want to retry
    """

# pylint: disable=too-many-instance-attributes
class RelukkoClient:
    """
    TBD
    """
    def __init__(
            self, base_url: Union[Url, str], api_key:str, **kwargs) -> None:
        """
        TBD
        """
        self.session = requests.Session()
        self.api_key = api_key
        self.tries=4
        self.delay=5
        self.backoff=2.0
        self.max_delay=None
        self.exceptions = (
            requests.ConnectionError,
            RelukkoDoRetry,
        )
        self._setup_session(api_key, **kwargs)
        self._setup_http_adapters_retry(**kwargs)
        self.acquire_modulo = 100
        self.acquire_wait_for_timeout = 2
        self.disable_websocket = False
        self.raise_when_acquire_fails = True
        self.ws_ping_interval = 60
        self.ws_ping_timeout = 20
        self.ws_wait_for_timeout = 2
        self._setup_pyrelukko_kwargs(**kwargs)

        self.base_url = self._setup_base_url(base_url)
        self.ws_url = self._setup_ws_url(str(self.base_url))
        self.ssl_ctx: ssl.SSLContext = None
        self._setup_ssl_ctx(**kwargs)

        # event for websocket thread to signal it got a message
        self.message_received = threading.Event()
        # As long as it's set the websocket thread runs
        self.ws_running = threading.Event()
        self.ws_listener: threading.Thread = None

    def reconfigure_relukko(
            self, base_url: Union[Url, str]=None, api_key: str=None, **kwargs):
        """
        TBD
        """
        self.api_key = api_key or self.api_key
        self._setup_session(self.api_key, **kwargs)
        self._setup_http_adapters_retry(**kwargs)
        self.base_url = self._setup_base_url(base_url or self.base_url)
        self.ws_url = self._setup_ws_url(str(self.base_url))
        self._setup_ssl_ctx(**kwargs)
        self._setup_pyrelukko_kwargs(**kwargs)

    def _setup_pyrelukko_kwargs(self, **kwargs):
        for kwarg in OWN_KWARGS:
            setattr(
                self,
                kwarg,
                kwargs.get(kwarg, getattr(self, kwarg))
            )

    def _setup_http_adapters_retry(self, **kwargs):
        for _, http_adapter in self.session.adapters.items():
            http_retry: Retry = http_adapter.max_retries
            for key, value in kwargs.items():
                if hasattr(http_retry, key):
                    setattr(http_retry, key, value)
            http_adapter.max_retries = http_retry

    def _setup_session(self, api_key: str, **kwargs):
        self.session.headers['X-api-Key'] = api_key
        for key, value in kwargs.items():
            if hasattr(self.session, key):
                setattr(self.session, key, value)

    def _setup_ssl_ctx(self, **kwargs) -> Union[ssl.SSLContext, None]:
        if self.ws_url.scheme == "wss":
            if self.ssl_ctx is None:
                self.ssl_ctx = ssl.create_default_context(
                    ssl.Purpose.SERVER_AUTH)
            for kwarg in SSL_KWARGS:
                setattr(
                    self.ssl_ctx,
                    kwarg,
                    kwargs.get(kwarg, getattr(self.ssl_ctx, kwarg)))

            # Try to behave like requests library and take *_CA_BUNDLE env vars
            # into account.
            ca_bundle = (
                os.environ.get("REQUESTS_CA_BUNDLE")
                or os.environ.get("CURL_CA_BUNDLE"))

            ca_bundle_file = None
            ca_bundle_path = None
            if ca_bundle is not None:
                ca_bundle = Path(ca_bundle)
                ca_bundle_file = ca_bundle if ca_bundle.is_file() else None
                ca_bundle_path = ca_bundle if ca_bundle.is_dir() else None

            # values from kwargs take precedence env vars
            ca_file = kwargs.get('cafile', ca_bundle_file)
            ca_path = kwargs.get('capath', f"{ca_bundle_path}/")
            ca_data = kwargs.get('cadata')

            if ca_file or ca_path or ca_data:
                self.ssl_ctx.load_verify_locations(
                    cafile=ca_file, capath=ca_path, cadata=ca_data)
        else:
            self.ssl_ctx = None

    def _setup_ws_url(self, ws_url: str) -> Url:
        url = ws_url.replace("http", "ws", 1)
        return parse_url(f"{url}/ws/broadcast")

    def _setup_base_url(self, base_url: Union[Url, str]) -> Url:
        if isinstance(base_url, str):
            base_url = parse_url(base_url)
        if not isinstance(base_url, Url):
            raise ValueError("must be URL or string!")

        return base_url

    async def _websocket_listener(self):
        """
        The WebSocket thread, which waits for messages from Relukko and
        notifies the HTTP thread in case deletions happend, so the HTTP
        can retry to get the lock. Does not verify the wanted lock got
        deleted yet.
        """
        additional_headers = { "X-API-KEY": self.api_key }
        async with ws_connect(
            str(self.ws_url),
            additional_headers=additional_headers,
            ssl=self.ssl_ctx,
            logger=logger,
            ping_interval=self.ws_ping_interval,
            ping_timeout=self.ws_ping_timeout,
        ) as websocket:
            while self.ws_running.is_set():
                try:
                    ws_message = await asyncio.wait_for(
                        websocket.recv(), timeout=self.ws_wait_for_timeout)
                    if ws_message:
                        logger.debug("Received message: '%s'", ws_message)
                        msg: Dict = json.loads(ws_message)
                        if msg.get('deleted'):
                            # Signal the HTTP thread to wake up
                            self.message_received.set()
                except TimeoutError:
                    # no messages, try in a moment again...
                    time.sleep(0.5)
                except WsConnectionClosed:
                    logger.error("Lost WS connection!")
                    continue

    def _acquire_relukko(
            self, url: Union[Url, str], max_run_time: int,
            payload: Dict, _thread_store: List):
        """
        The HTTP thread which tries to create the Relukko lock.
        """

        start_time = time.time()
        loop_counter = 0
        got_message = False
        res = None
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_run_time:
                self.ws_running.clear()
                _thread_store.insert(0, None)
                break
            # If self.message_recieved is True try to get lock ASAP!
            # Otherwise only in every Xth run in case websocket broke.
            if got_message or loop_counter % self.acquire_modulo == 0:
                try:
                    res = self._make_request(
                        url=url, method="POST", payload=payload)
                except (
                    *self.exceptions, RuntimeError, requests.HTTPError) as e:
                    logger.warning("Last exception was: %s!\nGiving up!", e)
                    _thread_store.insert(0, e)
                    break
            loop_counter += 1
            if res is None:
                # Conflict 409
                got_message = self.message_received.wait(
                    timeout=self.acquire_wait_for_timeout)
                self.message_received.clear()
                continue

            _thread_store.insert(0, res)
            self.ws_running.clear()
            break

    def _check_response(self, response: requests.Response):
        match response.status_code:
            case 200 | 201 | 404 | 422:
                return response.json()
            case 400 | 403:
                err = response.json()
                logger.warning("4xx HTTP Error [%d](%s) - %s:%s",
                    response.status_code, response.reason,
                    str(err.get('status')), err.get('message'))
                response.raise_for_status()
            case 409:
                err = response.json()
                logger.warning("409 HTTP Error [%d](%s) - %s:%s",
                    response.status_code, response.reason,
                    str(err.get('status')), err.get('message'))
                return None
            case 500 | 502 | 503 | 504:
                logger.warning("[%d](%s) %s",
                    response.status_code, response.reason, response.text)
                raise RelukkoDoRetry(
                    f"5xx HTTP Error: [{response.status_code}]"
                    f"({response.reason})")
            case _:
                logger.warning("[%d](%s) %s",
                    response.status_code, response.reason, response.text)
                raise RuntimeError(
                    f"Give up: [{response.status_code}]({response.reason})")

    def _make_request(
            self,
            url: str,
            method: str,
            payload: Dict=None) -> requests.Response:


        @retry(logger, exceptions=self.exceptions, tries=self.tries,
               delay=self.delay, backoff=self.backoff,
               max_delay=self.max_delay)
        def _do_request():
            response = self.session.request(
                method=method,
                url=url,
                json=payload,
            )
            return self._check_response(response)

        return _do_request()

    def acquire_relukko(self, lock_name, creator, max_run_time):
        """
        TBD
        """
        payload = {
            "lock_name": lock_name,
            "creator": creator,
        }

        url = f"{self.base_url}/v1/locks/"

        if not self.disable_websocket:
            self.ws_running.set()
            self.ws_listener = threading.Thread(
                target=asyncio.run, args=(self._websocket_listener(),))
            self.ws_listener.start()

        thread_store = []
        http_thread = threading.Thread(
            target=self._acquire_relukko,
            args=(url, max_run_time, payload, thread_store))
        http_thread.start()
        http_thread.join()

        if not self.disable_websocket:
            self.ws_listener.join()

        if thread_store:
            if (
                self.raise_when_acquire_fails
                and isinstance(thread_store[0], Exception)
            ):
                raise thread_store[0]
            return thread_store[0]
        return None

    def get_lock(self, lock_id: str) -> Dict:
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}"
        return self._make_request(url, "GET")

    def get_locks(self)  -> List:
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/"
        return self._make_request(url, "GET")

    def update_relukko(
            self, lock_id: str, creator: str=None, expires_at: datetime=None):
        """
        TBD
        """
        if isinstance(expires_at, datetime):
            expires_at = expires_at.isoformat()
        elif expires_at is not None:
            raise ValueError("has to be datetime!")

        payload = {
            "creator": creator,
            "expires_at": expires_at,
        }
        url = f"{self.base_url}/v1/locks/{lock_id}"
        return self._make_request(url, "PUT", payload)

    def delete_relukko(self, lock_id: str):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}"
        return self._make_request(url, "DELETE")

    def keep_relukko_alive(self, lock_id: str):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/keep_alive"
        return self._make_request(url, "GET")

    def keep_relukko_alive_put(self, lock_id: str, seconds: int):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/keep_alive"
        payload = {
            "seconds": seconds
        }
        return self._make_request(url, "PUT", payload)

    def add_to_expires_at_time(self, lock_id: str):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/add_to_expire_at"
        return self._make_request(url, "GET")

    def add_to_expires_at_time_put(self, lock_id: str, seconds: int):
        """
        TBD
        """
        url = f"{self.base_url}/v1/locks/{lock_id}/add_to_expire_at"
        payload = {
            "seconds": seconds
        }
        return self._make_request(url, "PUT", payload)
