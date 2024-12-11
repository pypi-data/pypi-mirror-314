import pytest
from mock import patch

import statsdecor
from statsdecor.context import StatsContext


class _DerivedContext(StatsContext):
    def __init__(self):
        super(_DerivedContext, self).__init__('test.hello')
        self.add_tag('always', 'yup')

    def exit_hook(self, a, b, c):
        self.add_tag('exit', 'yup')
        if b is None:
            self.add_tag('exception', 'none')
        else:
            self.add_tag('exception', 'yes')


class _BadContext(StatsContext):
    def __init__(self):
        super(_BadContext, self).__init__('test.badly')
        self.add_tag('always', 'badly')

    def exit_hook(self, a, b, c):
        raise Exception("derp derp derp")


class _TestException(Exception):
    pass


class TestStatsContext(object):
    tags = ['DogStatsd_does_tags!']
    vendor = 'datadog'

    @pytest.fixture(autouse=True)
    def client_configure(self):
        statsdecor.configure(vendor=self.vendor)

    @patch('datadog.dogstatsd.DogStatsd.increment')
    @patch('datadog.dogstatsd.DogStatsd.timing')
    def test_naked(self, timing, increment):
        s = StatsContext('test.naked', tags=['invocation:tag'])
        with s as s2:
            increment.assert_called_with(
                'test.naked.attempted',
                tags=['invocation:tag']
            )
            s2.add_tag('newtag', 'yes')

        increment.assert_called_with(
            'test.naked.completed',
            tags=['invocation:tag', 'newtag:yes']
        )
        print(repr(timing.call_args))
        print(repr(timing.call_args[0]))
        timing.assert_called()
        assert timing.call_args[1]['metric'] == 'test.naked.duration'
        assert timing.call_args[1]['value'] > 0
        assert timing.call_args[1]['tags'] == ['invocation:tag', 'newtag:yes']

    @patch('datadog.dogstatsd.DogStatsd.increment')
    @patch('datadog.dogstatsd.DogStatsd.timing')
    def test_derived_greenpath(self, timing, increment):
        with _DerivedContext() as s2:
            increment.assert_called_with(
                'test.hello.attempted',
                tags=['always:yup']
            )
            s2.add_tag('newtag', 'yes')

        expected_tags = ['always:yup', 'newtag:yes', 'exit:yup', 'exception:none']
        increment.assert_called_with(
            'test.hello.completed',
            tags=expected_tags
        )
        print(repr(timing))
        assert timing.call_args[1]['metric'] == 'test.hello.duration'
        assert timing.call_args[1]['value'] > 0
        assert timing.call_args[1]['tags'] == expected_tags

    @patch('datadog.dogstatsd.DogStatsd.increment')
    @patch('datadog.dogstatsd.DogStatsd.timing')
    def test_derived_exception(self, timing, increment):
        try:
            with _DerivedContext() as s2:
                increment.assert_called_with(
                    'test.hello.attempted',
                    tags=['always:yup']
                )
                s2.add_tag('newtag', 'yes')
                raise _TestException("this didn't go well")
        except _TestException:
            assert True, 'exception passed through'
        else:
            assert False, 'exception swallowed by context manager'  # pragma: nocover

        expected_tags = ['always:yup', 'newtag:yes', 'exit:yup', 'exception:yes']
        increment.assert_called_with(
            'test.hello.completed',
            tags=expected_tags
        )
        assert timing.call_args[1]['metric'] == 'test.hello.duration'
        assert timing.call_args[1]['value'] > 0
        assert timing.call_args[1]['tags'] == expected_tags

    @patch('datadog.dogstatsd.DogStatsd.increment')
    @patch('datadog.dogstatsd.DogStatsd.timing')
    def test_derived_raised_exception_itself(self, timing, increment):
        with _BadContext() as s2:
            increment.assert_called_with(
                'test.badly.attempted',
                tags=['always:badly']
            )
            s2.add_tag('newtag', 'yes')

        expected_tags = ['always:badly', 'newtag:yes']
        increment.assert_called_with(
            'test.badly.completed',
            tags=expected_tags
        )
        assert timing.call_args[1]['metric'] == 'test.badly.duration'
        assert timing.call_args[1]['value'] > 0
        assert timing.call_args[1]['tags'] == expected_tags
