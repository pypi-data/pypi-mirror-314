from contextlib import contextmanager
from timeit import default_timer as timer

from long_task_printer.unlimited_sequence import UnlimitedSequence
from long_task_printer.limited_sequence import LimitedSequence
from long_task_printer.formatting import format_time


@contextmanager
def print_with_time(message):
    """
    Run the given block of code, printing the message with timing information.
    Example usage:

        with print_with_time("Working on a thing"):
            thing_work()

    This prints:

        Working on a thing...
        Working on a thing DONE: 2.1s
    """
    print("{}...".format(message))

    start_time = timer()
    yield
    end_time = timer()

    print("{} DONE: {}".format(message, format_time(end_time - start_time)))


class LongTask():
    """
    Used to measure the running time of parts of a long-running task and output
    an estimation based on the average of the last 1-100 measurements.

    Example usage:

        long_task = LongTask(total_count=Product.count())

        for product in fetch_products():
            if product.not_something_we_want_to_process():
                long_task.skip(1)
                continue

            with long_task.measure() as progress:
                print(f"[{progress}] Product {product.id}")
                product.calculate_interesting_stats()

    Example output:
        [0000/1000, 000%, t/i: ?s, ETA: ?s] Product 1
        ...
        [0038/1000, 004%, t/i: 0.5s, ETA: 8m:00s] Product 39
        [0039/1000, 004%, t/i: 0.5s, ETA: 7m:58s] Product 40
        [0040/1000, 004%, t/i: 0.5s, ETA: 7m:57s] Product 41
        ...
        [0999/1000, 100%, t/i: 0.5s, ETA: 1s] Product 1000
    """
    def __init__(self, total_count=None, min_samples=1, max_samples=100, formatter=None):
        if total_count is None:
            self.sequence = UnlimitedSequence(min_samples, max_samples, formatter)
        else:
            self.sequence = LimitedSequence(total_count, min_samples, max_samples, formatter)

    @contextmanager
    def measure(self):
        """
        Run the given block of code, yielding a sequence object that holds progress
        information. Example usage:

            with long_task.measure() as progress:
                print(progress)
                long_running_task()

        The time it takes to run the block will be recorded as the next measurement.
        """
        start_time = timer()
        yield self.sequence
        end_time = timer()

        self.sequence.push(end_time - start_time)

    def skip(self, n=1):
        """
        Skips the given number of loops (will likely be 1), updating the
        estimations appropriately.
        """
        self.sequence.skip(n)

    def elapsed_time(self):
        """
        Returns the time since the sequence was started, formatted like all the
        other durations. Useful for a final message to compare initial estimation
        to actual elapsed time.
        """
        return self.sequence.elapsed_time()
