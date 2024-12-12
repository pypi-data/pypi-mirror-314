from datetime import datetime

from long_task_printer.formatting import format_time
from long_task_printer.error import Error


class LimitedSequence:
    def __init__(self, total_count, min_samples=1, max_samples=100, formatter=None):
        """
        Creates a new LimitedSequence with the given parameters:

        - total_count: The expected number of loops.

        - min_samples: The number of samples to collect before attempting to
          calculate a time per iteration. Default: 1

        - max_samples: The maximum number of measurements to collect and average.
          Default: 100.

        - formatter: A callable that accepts the sequence object and returns a
          custom formatted string.

        """
        self.total_count = total_count
        self.min_samples = min_samples
        self.max_samples = max_samples
        self.formatter = formatter

        if min_samples <= 0:
            raise Error("min_samples needs to be a positive number")
        if max_samples <= min_samples:
            raise Error("max_samples needs to be larger than min_samples")

        # The current loop index, starts at 0
        self.current = 0

        # The time the object was created
        self.start_time = datetime.now()
        self.total_count_digits = len(str(total_count))

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

    def skip(self, n):
        """
        Skips an iteration, updating the total count and ETA
        """
        self.total_count -= n

    def __str__(self):
        """
        Outputs a textual representation of the current state of the
        LimitedSequence. Shows:

        - the current number of iterations and the total count
        - completion level in percentage
        - how long a single iteration takes
        - estimated time of arrival (ETA) -- time until it's done

        A custom `formatter` provided at construction time overrides this default
        output.

        If the "current" number of iterations goes over the total count, an ETA
        can't be shown anymore, so it'll just be the current number over the
        expected one, and the time per iteration.
        """
        if self.formatter is not None:
            return str(self.formatter(self))

        if self.current > self.total_count:
            return ', '.join([
                f"{self.current} (expected {self.total_count})",
                f"t/i: {format_time(self.per_iteration())}",
                "ETA: ???",
            ])

        return ', '.join([
            f"{self.current:0{self.total_count_digits}}/{self.total_count}",
            f"{round((self.current / self.total_count) * 100):03}%",
            f"t/i: {format_time(self.per_iteration())}",
            f"ETA: {format_time(self.eta())}",
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
        Returns an estimation for the Estimated Time of Arrival (time until
        done).

        Calculated by multiplying the average time per iteration with the
        remaining number of loops.
        """
        if len(self.measurements) < self.min_samples:
            return None

        remaining_time = self.per_iteration() * (self.total_count - self.current)
        return round(remaining_time, 2)

    def elapsed_time(self):
        """
        Returns the time since the object was instantiated, formatted like all
        the other durations.
        """
        delta = datetime.now() - self.start_time
        return format_time(delta.seconds)


def _average(collection):
    return sum(collection) / len(collection)
