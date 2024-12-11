from statsdecor import client
import logging
from time import time


_log = logging.getLogger(__name__)


class StatsContext(object):
    """
        A context manager used for timing and tagging code.  On entering the context,
        this metric is emitted:

            count <metric_base>.attempted with <base_tags>

        where `base_tags` is the list passed as `tags` to the constructor.
        On completition:

            time <metric_base>.duration with <base_tags+added_tags>
            count <metric_base>.completed with <tags+added_tags>

        where "added_tags" are all tags added by calling `add_tags()`.  This
        can be done at any time inside the context.

        One way to use this is to extend StatsContext for each use.  The
        constructor is a good place to set default tags and the base metric
        name.  `exit_hook()` is a great place to classify unhandled exceptions
        into categories.

        For example, it can be used to create a wrapper around communication
        client library to collect response time and error rate metrics.  Since
        most calls to a the same client libraries typically indicate errors
        in the same way, one custom StatsContext class may be sufficient for
        all client calls.

        (There's a full example in the README.md)
    """

    def __init__(self, metric_base, tags=None, stats=None):
        """
            metric_base is add to the beginning of the "attempted", "duration", and "completed" metrics emited.

            tags is a list of string tags (in the format ["key:value", ..])
        """
        self._metric_base = metric_base

        self._tags = tags or []

        self._metric_attempted = '{}.attempted'.format(self._metric_base)
        self._metric_duration = '{}.duration'.format(self._metric_base)
        self._metric_completed = '{}.completed'.format(self._metric_base)

        self._stats = stats or client()

        self._elapsed = None

    def add_tag(self, key, value):
        """ Adds a datadog tag to the metrics emitted.

        Syntatic sugar equivalent to:

            add_tags('{}.{}'.format(key, value))
        """

        self.add_tags('{}:{}'.format(key, value))

    def add_tags(self, *tags):
        """ Adds a datadog tag to the metrics emitted.

        Tags added before the context begins are included in all metrics.
        Tags added before the context finished are included in the 'completed' and 'duration' metrics.
        """
        self._tags.extend(tags)

    def exit_hook(self, exc_type, exc_val, exc_tb):
        """ Called on exit.  By default does nothing.

        Child classes should override this method and translate the exceptions thrown
        (or lack of exceptions thrown) into metric tags.
        """

        pass

    def _start_timer(self):
        self._start = time()

    def _stop_timer(self):
        self._elapsed = time() - self._start

    def __enter__(self):
        self._stats.increment(self._metric_attempted, tags=self._tags)
        self._start_timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_timer()
        try:
            self.exit_hook(exc_type, exc_val, exc_tb)
        except Exception:
            # swallow errors--we don't want to complicate exception handling in the main
            # program flow.
            _log.exception("warning: Unhandled expcetion in StatsContext exit hook (ignoring)")

        self._stats.timing(self._metric_duration, self._elapsed, tags=self._tags)
        self._stats.increment(self._metric_completed, tags=self._tags)
        _log.debug('Metrics sent: {}, tags={}, elapsed time={}'.format(
            self._metric_base,
            ','.join(self._tags),
            self._elapsed
        ))
        return False
