"""
TBD
"""
import time
from functools import wraps


# pylint: disable=too-many-arguments,too-many-positional-arguments
def retry(logger, exceptions, tries=4, delay=5,
          backoff=2.0, max_delay=None):
    """
    Retry calling the decorated function using an exponential backoff.
    https://www.calazan.com/retry-decorator-for-python-3/

    :param exceptions: The exception to check. may be a tuple of
     exceptions to check.
    :param tries: Number of times to try (not retry) before giving up.
    :param delay: Initial delay between retries in seconds.
    :param backoff: Backoff multiplier (e.g. value of 2 will double the delay
     each retry).
    :param max_delay: maximum value for delay
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            remaining_tries, retry_delay = tries, delay
            while remaining_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions:
                    remaining_tries -= 1
                    logger.warning('(%i/%i): Retrying in %i seconds...',
                        tries - remaining_tries,
                        tries,
                        retry_delay,
                    )
                    time.sleep(retry_delay)
                    if max_delay is not None:
                        retry_delay = min(retry_delay*backoff, max_delay)
                    else:
                        retry_delay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry
