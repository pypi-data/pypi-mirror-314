from mock import patch, Mock


def stub_client(client_class, path='statsdecor.client'):
    """Factory for StubClient context managers"""
    return StubClient(path, client_class)


class StubClient(object):
    """Basic context manager that handles
    stubbing out the statsd client factory in the
    library.
    """
    def __init__(self, path, client_class):
        self.patcher = patch(path)
        self.client_class = client_class

    def __enter__(self):
        self.client = Mock(spec=self.client_class)
        stub_func = self.patcher.start()
        stub_func.return_value = self.client
        return self

    def __exit__(self, ty, value, traceback):
        self.patcher.stop()
