from functools import wraps
from statsdecor import client


def increment(name, tags=None):
    """Function decorator for incrementing a statsd stat whenever
    a function is invoked.

    >>> from statsdecor.decorators import increment
    >>> @increment('my.metric')
    >>> def my_func():
    >>>     pass
    """
    def wrap(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            stats = client()
            ret = f(*args, **kwargs)
            stats.incr(name, tags=tags)
            return ret
        return decorator
    return wrap


def decrement(name, tags=None):
    """Function decorator for decrementing a statsd stat whenever
    a function is invoked.

    >>> from statsdecor.decorators import decrement
    >>> @decrement('my.metric')
    >>> def my_func():
    >>>     pass
    """
    def wrap(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            stats = client()
            ret = f(*args, **kwargs)
            stats.decr(name, tags=tags)
            return ret
        return decorator
    return wrap


def timed(name, tags=None):
    """Function decorator for tracking timing information
    on a function's invocation.

    >>> from statsdecor.decorators import timed
    >>> @timed('my.metric')
    >>> def my_func():
    >>>     pass
    """
    def wrap(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            stats = client()
            with stats.timer(name, tags=tags):
                return f(*args, **kwargs)
        return decorator
    return wrap
