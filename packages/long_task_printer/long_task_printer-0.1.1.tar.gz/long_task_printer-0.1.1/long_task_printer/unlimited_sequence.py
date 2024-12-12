from datetime import datetime

from long_task_printer.formatting import format_time
from long_task_printer.error import Error


class UnlimitedSequence:
    def __init__(self, min_samples=1, max_samples=100, formatter=None):
        """
        Creates a new UnlimitedSequence with the given parameters:

        - min_samples: The number of samples to collect before attempting to
          calculate a time per iteration. Default: 1

        - max_samples: The maximum number of measurements to collect and
          average. Default: 100.

        - formatter: A callable that accepts the sequence object and returns a
          custom formatted string.
        """
        self.min_samples = min_samples
        self.max_samples = max_samples
        self.formatter = formatter

        if min_samples <= 0:
            raise Error("min_samples needs to be a positive number")
        if max_samples <= min_samples:
            raise Error("max_samples needs to be larger than min_samples")

        # The current loop index, starts at 1
        self.current = 1

        # The time the object was created
        self.start_time = datetime.now()

        self.measurements = []
        self.averages = []

    def push(self, duration):
        """
        Adds a duration in seconds to the internal storage of samples. Updates
        averages accordingly.
        """
        self.current += 1
        self.measurements.append(duration)

        # only keep last `max_samples`:
        if len(self.measurements) > self.max_samples:
            self.measurements.remove(0)

        self.averages.append(_average(self.measurements))
        self.averages = [value for value in self.averages if value is not None]

        # only keep last `max_samples`
        if len(self.averages) > self.max_samples:
            self.averages.remove(0)

    def skip(self, _n):
        """
        "Skips" an iteration, which, in the context of an UnlimitedSequence is
        a no-op.
        """
        pass

    def __str__(self):
        """
        Outputs a textual representation of the current state of the
        UnlimitedSequence. Shows:

        - the current (1-indexed) number of iterations
        - how long since the start time
        - how long a single iteration takes

        A custom `formatter` provided at construction time overrides this
        default output.
        """
        if self.formatter is not None:
            return str(self.formatter(self))

        return ', '.join([
            f"{self.current}",
            f"t: {self.elapsed_time()}",
            f"t/i: {format_time(self.per_iteration())}",
        ])

    def per_iteration(self):
        """
        Returns an estimation for the time per single iteration. Implemented as
        an average of averages to provide a smoother gradient from loop to
        loop.

        Returns nil if not enough samples have been collected yet.
        """
        if len(self.measurements) < self.min_samples:
            return None

        return _average(self.averages)

    def eta(self):
        """
        Is supposed to return an estimation for the Estimated Time of Arrival
        (time until done).

        For an UnlimitedSequence, this always returns nil.
        """
        pass

    def elapsed_time(self):
        """
        Returns the time since the object was instantiated, formatted like all
        the other durations.
        """
        delta = datetime.now() - self.start_time
        return format_time(delta.seconds)


def _average(collection):
    return sum(collection) / len(collection)
