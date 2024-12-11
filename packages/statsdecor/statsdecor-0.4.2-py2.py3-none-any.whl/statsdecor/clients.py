from datadog import DogStatsd
from statsd import StatsClient


class DogStatsdClient(DogStatsd):
    """Wrapper for Datadog's DogStatsd client

    For docs on the DogStatsd client, see
    http://datadogpy.readthedocs.io/en/latest/

    For the code, see
    https://github.com/DataDog/datadogpy/blob/master/datadog/dogstatsd/base.py
    """
    def incr(self, name, value=1, rate=1, tags=None):
        super(DogStatsdClient, self).increment(metric=name, value=value, tags=tags, sample_rate=rate)

    def decr(self, name, value=1, rate=1, tags=None):
        super(DogStatsdClient, self).decrement(metric=name, value=value, tags=tags, sample_rate=rate)

    def gauge(self, name, value=1, rate=1, tags=None):
        super(DogStatsdClient, self).gauge(metric=name, value=value, tags=tags, sample_rate=rate)

    def timing(self, name, value, tags=None, rate=1):
        super(DogStatsdClient, self).timing(metric=name, value=value, tags=tags, sample_rate=rate)

    def timer(self, name, tags=None):
        return super(DogStatsdClient, self).timed(metric=name, tags=tags)


class StatsdClient(StatsClient):
    """Wrapper for statsd client

    For docs on the statsd client, see
    http://statsd.readthedocs.org/en/latest/types.html

    For the code, see
    https://github.com/jsocol/pystatsd/blob/master/statsd/client.py
    """
    def incr(self, name, value=1, rate=1, tags=None):
        self._assert_no_tags(tags)
        super(StatsdClient, self).incr(stat=name, count=value, rate=rate)

    def decr(self, name, value=1, rate=1, tags=None):
        self._assert_no_tags(tags)
        super(StatsdClient, self).decr(stat=name, count=value, rate=rate)

    def gauge(self, name, value=1, rate=1, tags=None):
        self._assert_no_tags(tags)
        super(StatsdClient, self).gauge(stat=name, value=value, rate=rate)

    def timing(self, name, value=1, rate=1, tags=None):
        self._assert_no_tags(tags)
        super(StatsdClient, self).timing(stat=name, delta=value, rate=rate)

    def timer(self, name, tags=None):
        self._assert_no_tags(tags)
        return super(StatsdClient, self).timer(stat=name)

    def _assert_no_tags(self, tags):
        if tags:
            raise ValueError(u'Tagging is not supported by StatsdClient.\n tags: {}'.format(tags))
