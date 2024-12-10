import logging
import random
import time
from functools import partial
from typing import Any, Callable, Optional


def retry_call(
    f,
    fargs: Optional[Any] = None,
    fkwargs=None,
    exceptions=Exception,
    tries=-1,
    delay=0,
    max_delay=None,
    backoff=1,
    jitter=0,
    logger: Any = logging.getLogger(__name__),
) -> Any:
    """
    Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0. fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts. default: logging.getLogger("retry"). if None, logging is disabled.
    :returns: the result of the f function.
    """
    func = partial(f, *(fargs or list()), **fkwargs or dict())
    _tries, _delay = tries, delay
    while _tries:
        try:
            return func()
        except exceptions as e:
            _tries -= 1
            if not _tries:
                raise

            if logger is not None:
                logger.warning(f"{e.__class__.__name__}({e}), retrying in {_delay} seconds...")

            time.sleep(_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)


def retry(
    exceptions=Exception,
    tries=-1,
    delay=0,
    max_delay=None,
    backoff=1,
    jitter=0,
    logger: Any = logging.getLogger(__name__),
) -> Callable[..., Any]:
    def wrapper(f, *fargs, **fkwargs) -> Callable[..., Any]:
        return partial(
            retry_call,
            f=f,
            fargs=fargs,
            fkwargs=fkwargs,
            exceptions=exceptions,
            tries=tries,
            delay=delay,
            max_delay=max_delay,
            backoff=backoff,
            jitter=jitter,
            logger=logger,
        )

    return wrapper


__ALL__ = (
    "retry",
    "retry_call",
)
