import pytest
from mock import MagicMock

import statsdecor
import statsdecor.decorators as decorators
from statsdecor.clients import DogStatsdClient, StatsdClient
from tests.conftest import stub_client

NO_TAGS = None


def assert_arguments(args, kwargs):
    assert ('some', 'thing') == args
    assert {'key': 'value'} == kwargs


class BaseDecoratorTestCase(object):

    def test_increment__no_tags(self):
        @decorators.increment('a.metric')
        def test_fn(*args, **kwargs):
            assert_arguments(args, kwargs)

        with stub_client(self.client_class, 'statsdecor.decorators.client') as stub:
            test_fn('some', 'thing', key='value')
            stub.client.incr.assert_called_with('a.metric', tags=NO_TAGS)

    def test_increment__with_tags(self):
        @decorators.increment('a.metric', tags=self.tags)
        def test_fn(*args, **kwargs):
            assert_arguments(args, kwargs)

        with stub_client(self.client_class, 'statsdecor.decorators.client') as stub:
            test_fn('some', 'thing', key='value')
            stub.client.incr.assert_called_with('a.metric', tags=self.tags)

    def test_decrement__no_tags(self):
        @decorators.decrement('a.metric')
        def test_fn(*args, **kwargs):
            assert_arguments(args, kwargs)

        with stub_client(self.client_class, 'statsdecor.decorators.client') as stub:
            test_fn('some', 'thing', key='value')
            stub.client.decr.assert_called_with('a.metric', tags=NO_TAGS)

    def test_decrement__with_tags(self):
        @decorators.decrement('a.metric', tags=self.tags)
        def test_fn(*args, **kwargs):
            assert_arguments(args, kwargs)

        with stub_client(self.client_class, 'statsdecor.decorators.client') as stub:
            test_fn('some', 'thing', key='value')
            stub.client.decr.assert_called_with('a.metric', tags=self.tags)

    def test_timed__no_tags(self):
        @decorators.timed('a.metric')
        def test_fn(*args, **kwargs):
            assert_arguments(args, kwargs)

        with stub_client(self.client_class, 'statsdecor.decorators.client') as stub:
            # Stub out the timing context manager.
            stub.client.timer.return_value = MagicMock()
            test_fn('some', 'thing', key='value')
            stub.client.timer.assert_called_with('a.metric', tags=NO_TAGS)

    def test_timed__with_tags(self):
        @decorators.timed('a.metric', tags=self.tags)
        def test_fn(*args, **kwargs):
            assert_arguments(args, kwargs)

        with stub_client(self.client_class, 'statsdecor.decorators.client') as stub:
            # Stub out the timing context manager.
            stub.client.timer.return_value = MagicMock()
            test_fn('some', 'thing', key='value')
            stub.client.timer.assert_called_with('a.metric', tags=self.tags)


class TestStatsdDefaultClient(BaseDecoratorTestCase):
    tags = ['StatsClient_doesnt_do_tags!']
    client_class = StatsdClient

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure()


class TestDogStatsdClient(BaseDecoratorTestCase):
    tags = ['DogStatsd_does_tags!']
    vendor = 'datadog'
    client_class = DogStatsdClient

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure(vendor=self.vendor)
