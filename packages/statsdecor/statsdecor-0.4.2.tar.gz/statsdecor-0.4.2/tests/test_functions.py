import pytest
import statsd
from datadog import DogStatsd

import statsdecor
from statsdecor.clients import DogStatsdClient, StatsdClient
from tests.conftest import stub_client


class BaseFunctionTestCase(object):
    def test_incr(self):
        with stub_client(self.client_class) as stub:
            statsdecor.incr('a.metric')
            stub.client.incr.assert_called_with('a.metric', 1, 1, None)

    def test_incr__with_value_and_rate(self):
        with stub_client(self.client_class) as stub:
            statsdecor.incr('a.metric', 9, 0.1)
            stub.client.incr.assert_called_with('a.metric', 9, 0.1, None)

    def test_decr(self):
        with stub_client(self.client_class) as stub:
            statsdecor.decr('a.metric')
            stub.client.decr.assert_called_with('a.metric', 1, 1, None)

    def test_decr__with_value_and_rate(self):
        with stub_client(self.client_class) as stub:
            statsdecor.decr('a.metric', 9, 0.1)
            stub.client.decr.assert_called_with('a.metric', 9, 0.1, None)

    def test_gauge(self):
        with stub_client(self.client_class) as stub:
            statsdecor.gauge('a.metric', 8)
            stub.client.gauge.assert_called_with('a.metric', 8, 1, None)

    def test_gauge__with_value_and_rate(self):
        with stub_client(self.client_class) as stub:
            statsdecor.gauge('a.metric', 9, 0.1)
            stub.client.gauge.assert_called_with('a.metric', 9, 0.1, None)

    def test_timer(self):
        with stub_client(self.client_class) as stub:
            statsdecor.timer('a.metric')
            assert stub.client.timer.called, 'Should be called'

    def test_timing(self):
        with stub_client(self.client_class) as stub:
            statsdecor.timing('a.metric', 314159265359)
            stub.client.timing.assert_called_with(
                'a.metric',
                314159265359,
                rate=1,
                tags=None
            )

    def test_timing__with_value_and_rate(self):
        with stub_client(self.client_class) as stub:
            statsdecor.timing('a.metric', 314159265359, 0.1)
            stub.client.timing.assert_called_with(
                'a.metric',
                314159265359,
                rate=0.1,
                tags=None
            )

    def test_configure_and_create(self):
        raise NotImplementedError()


class TestStatsdDefaultClient(BaseFunctionTestCase):
    client_class = StatsdClient

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure(vendor='')

    def test_client_created_if_no_existing_client__with_no_config(self, monkeypatch):
        monkeypatch.setattr(statsdecor, '_stats_client', None)
        client = statsdecor.client()
        assert isinstance(client, statsd.StatsClient)

    def test_configure_and_create(self):
        statsdecor.configure(port=9999)
        client = statsdecor.client()
        assert client._addr[1] == 9999, 'port should match'
        assert not statsdecor.client_supports_tags()

    def test_configure_and_create__with_fields_not_in_whitelist(self):
        statsdecor.configure(random=1234, field=33, port=1234)
        client = statsdecor.client()
        assert isinstance(client, statsd.StatsClient)
        assert client._addr[1] == 1234, 'port should match'

    def test_should_not_support_tags(self):
        statsdecor.configure(port=9999)
        statsdecor.client()
        assert not statsdecor.client_supports_tags()


class TestDogStatsdClient(BaseFunctionTestCase):
    client_class = DogStatsdClient
    vendor = 'datadog'

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure(vendor=self.vendor)

    def test_configure_and_create(self):
        statsdecor.configure(port=9999)
        client = statsdecor.client()
        assert client.port == 9999, 'port should match'

    def test_configure_and_create__with_prefix(self):
        statsdecor.configure(prefix='statsdecor')
        client = statsdecor.client()
        assert client.namespace == 'statsdecor', 'namespace should match prefix'

    def test_configure_and_create__with_fields_not_in_whitelist(self):
        statsdecor.configure(maxudpsize=512)
        client = statsdecor.client()
        assert isinstance(client, DogStatsd)

    def test_should_support_tags(self):
        statsdecor.configure(port=9999)
        statsdecor.client()
        assert statsdecor.client_supports_tags()
