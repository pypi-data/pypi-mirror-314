import statsdecor
import pytest
from mock import patch
from datadog.dogstatsd.context import TimedContextManagerDecorator as DatadogTimer
from statsd.client.timer import Timer as StatsdTimer


DEFAULT_RATE = 1
DEFAULT_VALUE = 1
NO_TAGS = None


class TestStatsdDefaultClient(object):
    tags = ['StatsClient_doesnt_do_tags!']

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure(vendor='')

    @patch('statsd.client.StatsClient.incr')
    def test_incr_no_tag(self, mocked_super):
        statsdecor.incr('a.metric')
        mocked_super.assert_called_with(stat='a.metric', count=DEFAULT_VALUE, rate=DEFAULT_RATE)

    def test_incr_with_tag(self):
        with pytest.raises(ValueError):
            statsdecor.incr('a.metric', tags=self.tags)

    @patch('statsd.client.StatsClient.decr')
    def test_decr_no_tag(self, mocked_super):
        statsdecor.decr('a.metric')
        mocked_super.assert_called_with(stat='a.metric', count=DEFAULT_VALUE, rate=DEFAULT_RATE)

    def test_decr_with_tag(self):
        with pytest.raises(ValueError):
            statsdecor.decr('a.metric', tags=self.tags)

    @patch('statsd.client.StatsClient.gauge')
    def test_gauge_no_tag(self, mocked_super):
        statsdecor.gauge('a.metric', value=DEFAULT_VALUE)
        mocked_super.assert_called_with(stat='a.metric', value=DEFAULT_VALUE, rate=DEFAULT_RATE)

    def test_gauge_with_tag(self):
        with pytest.raises(ValueError):
            statsdecor.gauge('a.metric', value=DEFAULT_VALUE, tags=self.tags)

    @patch('statsd.client.StatsClient.timing')
    def test_timing_no_tag(self, mocked_super):
        statsdecor.timing('a.metric', delta=DEFAULT_VALUE)
        mocked_super.assert_called_with(stat='a.metric', delta=DEFAULT_VALUE, rate=DEFAULT_RATE)

    def test_timing_with_tag(self):
        with pytest.raises(ValueError):
            statsdecor.timing('a.metric', delta=DEFAULT_VALUE, tags=self.tags)

    def test_timer_no_tag(self):
        assert isinstance(statsdecor.timer('a.metric'), StatsdTimer)

    def test_timer_with_tag(self):
        with pytest.raises(ValueError):
            statsdecor.timer('a.metric', tags=self.tags)


class TestDogStatsdClient(object):
    tags = ['DogStatsd_does_tags!']
    vendor = 'datadog'

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure(vendor=self.vendor)

    @patch('datadog.dogstatsd.DogStatsd.increment')
    def test_incr_no_tag(self, mocked_super):
        statsdecor.incr('a.metric')
        mocked_super.assert_called_with(metric='a.metric', value=DEFAULT_VALUE, tags=NO_TAGS, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.increment')
    def test_incr_with_tag(self, mocked_super):
        statsdecor.incr('a.metric', tags=self.tags)
        mocked_super.assert_called_with(
            metric='a.metric', value=DEFAULT_VALUE, tags=self.tags, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.decrement')
    def test_decr_no_tag(self, mocked_super):
        statsdecor.decr('a.metric')
        mocked_super.assert_called_with(metric='a.metric', value=DEFAULT_VALUE, tags=NO_TAGS, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.decrement')
    def test_decr_with_tag(self, mocked_super):
        statsdecor.decr('a.metric', tags=self.tags)
        mocked_super.assert_called_with(
            metric='a.metric', value=DEFAULT_VALUE, tags=self.tags, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.gauge')
    def test_gauge_no_tag(self, mocked_super):
        statsdecor.gauge('a.metric', value=DEFAULT_VALUE)
        mocked_super.assert_called_with(metric='a.metric', value=DEFAULT_VALUE, tags=NO_TAGS, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.gauge')
    def test_gauge_with_tag(self, mocked_super):
        statsdecor.gauge('a.metric', value=DEFAULT_VALUE, tags=self.tags)
        mocked_super.assert_called_with(
            metric='a.metric', value=DEFAULT_VALUE, tags=self.tags, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.timing')
    def test_timing_no_tag(self, mocked_super):
        statsdecor.timing('a.metric', delta=DEFAULT_VALUE)
        mocked_super.assert_called_with(metric='a.metric', value=DEFAULT_VALUE, tags=NO_TAGS, sample_rate=DEFAULT_RATE)

    @patch('datadog.dogstatsd.DogStatsd.timing')
    def test_timing_with_tag(self, mocked_super):
        statsdecor.timing('a.metric', delta=DEFAULT_VALUE, tags=self.tags)
        mocked_super.assert_called_with(
            metric='a.metric', value=DEFAULT_VALUE, tags=self.tags, sample_rate=DEFAULT_RATE)

    def test_timer_no_tag(self):
        assert isinstance(statsdecor.timer('a.metric'), DatadogTimer)

    def test_timer_with_tag(self):
        assert isinstance(statsdecor.timer('a.metric', tags=self.tags), DatadogTimer)
