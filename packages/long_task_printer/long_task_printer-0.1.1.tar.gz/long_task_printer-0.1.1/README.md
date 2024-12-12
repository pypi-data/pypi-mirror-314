*This is a python rewrite of my ruby tool [progressor](https://github.com/andrewradev/progressor), so some of the code and examples might not feel pythonic. It may change over time as I use it more.*

## Basic example

Here's an example long-running task:

```python
for product in fetch_products():
    if product.not_something_we_want_to_process():
        continue

    product.calculate_interesting_stats()
```

In order to understand how it's progressing, we might add some print statements:

```python
for product in fetch_products():
    if product.not_something_we_want_to_process():
        print(f"Skipping product: {product.id}")
        continue

    print(f"Working on product: {product.id}")
    product.calculate_interesting_stats()
```

This gives us some indication of progress, but no idea how much time is left. We could take a count and maintain a manual index, and then eyeball it based on how fast the numbers are adding up. LongTask automates that process:

```python
long_task = LongTask(total_count=Product.count())

for product in fetch_products():
    if product.not_something_we_want_to_process():
        long_task.skip(1)
        continue

    with long_task.measure() as progress:
        print(f"[{progress} Working on product: {product.id}")
        product.calculate_interesting_stats()
```

Each invocation of `measure` measures how long its block took and records it. The `progress` parameter is an object that can be converted to a string to provide progress information.

The output might look like this:

```
...
[0038/1000, (004%), t/i: 0.5s, ETA: 8m:00s] Product 38
[0039/1000, (004%), t/i: 0.5s, ETA: 7m:58s] Product 39
[0040/1000, (004%), t/i: 0.5s, ETA: 7m:57s] Product 40
...
```

You can check the documentation for the `LongTask` class for details on the methods you can call to get the individual pieces of data shown in the report.

## Limited and unlimited sequences

Initializing a `LongTask` with a provided `total_count=` parameter gives you a limited sequence, which can give you not only a progress report, but an estimation of when it'll be done:

```
[<current loop>/<total count>, (<progress>%), t/i: <time per iteration>, ETA: <time until it's done>]
```

The calculation is done by maintaining a list of measurements with a limited size, and a list of averages of those measurements. The average of averages is the "time per iteration" and it's multiplied by the remaining count to produce the estimation.

I can't really say how reliable this is, but it seems to provide smoothly changing estimations that seem more or less correct to me, for similarly-sized chunks of work per iteration.

**Not** providing a `total_count=` parameter leads to less available information:

```python
long_task = LongTask()

for _ in range(100):
    with long_task.measure() as progress:
        print(progress)
        time.sleep(random.random())
```

A sample of output might look like this:

```
...
11, t: 5.32s, t/i: 442.39ms
12, t: 5.58s, t/i: 446.11ms
...
```

The format is:

```
<current>, t: <time from start>, t/i: <time per iteration>
```

## Configuration

Apart from `total_count`, which is optional and affects the kind of sequence that will be stored, you can provide `min_samples` and `max_samples`. You can also provide a custom formatter:

```python
long_task = LongTask(
    total_count=1000,
    min_samples=5,
    max_samples=10,
    formatter=lambda p: p.eta()
)
```

The option `min_samples` determines how many loops the tool will wait until trying to produce an estimation. A higher number means no information in the beginning, but no wild fluctuations, either. It needs to be at least 1 and the default is 1.

The option `max_samples` is how many measurements will be retained. Those measurements will be averaged, and then those averages averaged to get a time-per-iteration estimate. A smaller number means giving more weight to later events, while a larger one would average over a larger amount of samples. The default is 100.

The `formatter` is a callback that gets a progress object as an argument and you can return your own string to output on every loop. Check `LimitedSequence` and `UnlimitedSequence` for the available methods and accessors you can use.

## Related work

This project is based on my ruby tool [progressor](https://github.com/andrewradev/progressor). In terms of other python libraries, there seem to be a few:

- [ProgressPrinter](https://pypi.org/project/ProgressPrinter/) shows an animated progress bar, which likely means it moves the cursor on top when outputting its progress. This project just gives you a string to print, which could sit in logs, inbetween other output, etc.
- [longtask](https://pypi.org/project/longtask/) gives you a different interface where you create a separate class to encapsulate your long-running task.
- [progressor](https://pypi.org/project/progressor/) uses scikit to estimate the remaining time and shows an animated progress bar
