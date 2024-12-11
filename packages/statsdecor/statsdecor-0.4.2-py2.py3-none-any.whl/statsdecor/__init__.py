import logging
from statsdecor.clients import (
    DogStatsdClient,
    StatsdClient
)

log = logging.getLogger(__name__)
_config = {}
_stats_client = None


def _create_client(**config):
    vendor = config.pop('vendor', None)

    if vendor == 'datadog':
        client_config = _create_client_config(config, {'host', 'port', 'use_ms'})
        client_config.update(namespace=config.get('prefix')) if config.get('prefix') else None
        return DogStatsdClient(**client_config)

    client_config = _create_client_config(config, {'host', 'port', 'prefix', 'maxudpsize'})
    return StatsdClient(**client_config)


def _create_client_config(raw_config, whitelist_fields):
    client_config = {
        field: raw_config.get(field) for field in whitelist_fields if raw_config.get(field)
    }
    return client_config


def configure(*args, **kwargs):
    """Configure the module level statsd client that will
    be used in all library operations.

    Frequently used from application initialization code.

    >>> import statsdecor
    >>> statsdecor.configure(
            host='localhost',
            port=8125,
            prefix='myapp',
            maxudpsize=25)
    """
    global _stats_client

    log.debug('statsd.configure(%s)' % kwargs)
    _config.update(kwargs)

    _stats_client = _create_client(**_config)


def client():
    """Get a client instance with the module level configuration."""
    if _stats_client is None:
        configure({})
    return _stats_client


def client_supports_tags():
    if isinstance(client(), DogStatsdClient):
        return True
    return False


def incr(name, value=1, rate=1, tags=None):
    """Increment a metric by value.

    >>> import statsdecor
    >>> statsdecor.incr('my.metric')
    """
    client().incr(name, value, rate, tags)


def decr(name, value=1, rate=1, tags=None):
    """Decrement a metric by value.

    >>> import statsdecor
    >>> statsdecor.decr('my.metric')
    """
    client().decr(name, value, rate, tags)


def gauge(name, value, rate=1, tags=None):
    """Set the value for a gauge.

    >>> import statsdecor
    >>> statsdecor.gauge('my.metric', 10)
    """
    client().gauge(name, value, rate, tags)


def timer(name, tags=None):
    """Time a block of code with a context manager.

    >>> import statsdecor
    >>> with statsdecor.timer('my.timer'):
    >>>     print('Some output')
    Some output
    """
    return client().timer(name, tags)


def timing(name, delta, rate=1, tags=None):
    """Sends new timing information. `delta` is in milliseconds.

    >>> import statsdecor
    >>> statsdecor.timing('my.metric', 314159265359)
    """
    return client().timing(name, delta, rate=rate, tags=tags)
