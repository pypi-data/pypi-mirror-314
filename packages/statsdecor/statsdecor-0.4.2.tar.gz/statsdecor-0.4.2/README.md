# Statsdecor

[![PyPI](https://img.shields.io/pypi/v/statsdecor)](https://pypi.org/project/statsdecor/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/statsdecor)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.txt)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/amcintosh/statsdecor/run-tests.yml?branch=main)](https://github.com/amcintosh/statsdecor/actions?query=workflow%3A%22Run+Tests%22)

A set of decorators and helper methods for adding statsd metrics to applications.

## Installation

You can use pip to install statsdecor:

```shell
pip install statsdecor
```

## Configuration

You must use `statsdecor.configure` to configure the internal statsd client before
calling other methods:

```python
import statsdecor

statsdecor.configure(host='localhost', prefix='superapp.')
```

Configuration is generally setup during your application's bootstrap. Once
set configuration values are re-used in all clients that `statsdecor` creates.

By default Statsdecor uses the [statsd](https://pypi.org/project/statsd/) client library,
however it can be configured to use the [datadog](https://pypi.org/project/datadog/) client:

```python
import statsdecor

statsdecor.configure(host='localhost', prefix='superapp.', vendor='datadog')
```

The datadog client supports [tagging metrics](https://statsd.readthedocs.io/en/stable/tags.html) (see Usage).

## Usage

You can track metrics with either the module functions, or decorators. Incrementing
and decrementing counters looks like:

### Metric functions

```python
import statsdecor

statsdecor.incr('save.succeeded')
statsdecor.decr('attempts.remaining')
statsdecor.gauge('sessions.active', 9001)
```

When using the datadog client, Statsdecor supports tagging metrics:

```python
statsdecor.incr('save.succeeded', tags=['DogStatsd_does_tags'])
```

Counters and timers can also be set through decorators:

```python
import statsdecor.decorators as stats

@stats.increment('save.succeeded')
def save(self):
    pass

@stats.decrement('attempts.remaining')
def attempt():
    pass

@stats.timed('api_request.duration')
def perform_request(self, req)
    pass
```

When using decorators, metrics are only tracked if the decorated function
does not raise an error.

### Context

When using a [statsd client that supports tagging metrics](https://statsd.readthedocs.io/en/stable/tags.html),
Statsdecor includes a context manager that can help measure latency and volume while using metric tags to
classify their success & failure. For example, suppose you are making a call to a remote service and wish
to write a wrapper that collects latency, volume and failure metrics.

With our knowledge about how the client library indicates errors we can make a context manager
based on StatsContext:

```python
from statsdecor.context import StatsContext

class FoobarClientMetrics(StatsContext):
    def __init__(self, tags=None):
        tags = list(tags or [])
        tags += ['caller:example_1']
        super(ThingyStatsContext, self).__self__('thingy_client', tags=tags)

    def exit_hook(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.add_tags('result:failure')
        else:
            self.add_tags('result:success')

        # Bonus: since we have the exception, classify the error type
        if isinstance(exc_val, PermissionDenied):
            self.add_tags('error:permissiondenied')
        elif isinstance(exc_val, TimeOut):
            self.add_tags('error:timeout')
        elif exc_val is not None:
            self.add_tags('error:exception')

```

Now writing wrapper functions with metrics is simple:

```python
def foobar_get_clients(**args):
    with FoobarClientMetrics(tags=['method:get_clients']) as stats:
        result = call_foobar_get_client(**args)

        # We know all foo methods return result['status_code'] so let's
        # add a status_code tag!
        stats.add_tags('status_code:{}'.format(result["status_code"]'))
        return result

def foobar_add_client(**args):
    with FoobarClientMetrics(tags=['method:add_client']) as stats:
        result = call_foobar_add_client(**args)
        stats.add_tags('status_code:{}'.format(result["status_code"]'))
        return result
```

Now we can graph:

* volume of calls grouped by the `method` tag
* average response time, excluding errors (timeouts will no longer skew the average)
* volume of errors grouped by method, and/or type

## Development

### Testing

```shell
make lint
make test
```

### Releasing

statsdecor uses [semver](https://semver.org) for version numbers. Before tagging,
check for all changes since the last tag for breaking changes, new features,
and/or bugfixes.

To tag the new version:

```shell
make tag VERSION_PART=major|minor|patch
```

Proceed to github.com/amcintosh/statsdecor/releases and create a new release with the tag.
Github actions should publish to pypi automatically.
