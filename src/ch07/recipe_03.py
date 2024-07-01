# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Designing classes with lots of processing


# Subection: Getting ready

from collections import Counter

data = Counter({7: 80,
         6: 67,
         8: 62,
         9: 50,
         15: 34,
         11: 33,
         18: 32,
         10: 32,
         16: 29,
         14: 28,
         13: 27,
         17: 22,
         12: 20,
         5: 18,
         4: 11,
         19: 8,
         2: 3,
         3: 2,
         1: 1})

# Subection: How to do it...

from collections import Counter
import math

class CounterStatistics:
    def __init__(self, raw_counter: Counter[int]) ->  None:
        self.raw_counter = raw_counter
        self.mean = self.compute_mean()
        self.stddev = self.compute_stddev()

    def compute_mean(self) -> float:
        total, count = 0.0, 0
        for value, frequency in self.raw_counter.items():
            total += value * frequency
            count += frequency
        return total / count

    def compute_stddev(self) -> float:
        total, count = 0.0, 0
        for value, frequency in self.raw_counter.items():
            total += frequency * (value - self.mean) ** 2
            count += frequency
        return math.sqrt(total / (count - 1))

    def add(self, value: int) -> None:
        self.raw_counter[value] += 1
        self.mean = self.compute_mean()
        self.stddev = self.compute_stddev()

test_example_2_7 = """
>>> from pathlib import Path
>>> import csv
>>> from collections import Counter

>>> data_path = Path.cwd() / "data" / "binned.csv"
>>> with data_path.open() as data_file:
...     reader = csv.DictReader(data_file)
...     extract = {
...         int(row['size_code']): int(row['frequency'])
...         for row in reader
...     }
>>> data = Counter(extract)
"""

test_example_2_8 = """
>>> stats = CounterStatistics(data)
>>> print(f"Mean: {stats.mean:.1f}")
Mean: 10.4
>>> print(f"Standard Deviation: {stats.stddev:.2f}")
Standard Deviation: 4.17
"""

# Subection: There's more...

class CounterStatistics2:

    def __init__(self, counter: Counter[int] | None = None) -> None:
        if counter is not None:
            self.raw_counter = counter
            self.count = sum(
                self.raw_counter[k] for k in self.raw_counter)
            self.sum = sum(
                self.raw_counter[k] * k for k in self.raw_counter)
            self.sum2 = sum(
                self.raw_counter[k] * k ** 2
                for k in self.raw_counter)
            self.mean: float | None = self.sum / self.count
            self.stddev: float | None = math.sqrt(
                (self.sum2 - self.sum ** 2 / self.count)
                / (self.count - 1)
            )

        else:
            self.raw_counter = Counter()
            self.count = 0
            self.sum = 0
            self.sum2 = 0
            self.mean = None
            self.stddev = None

    def add(self, value: int) -> None:
        self.raw_counter[value] += 1
        self.count += 1
        self.sum += value
        self.sum2 += value ** 2
        self.mean = self.sum / self.count
        if self.count > 1:
            self.stddev = math.sqrt(
                (self.sum2 - self.sum ** 2 / self.count)
                / (self.count - 1)
            )


# End of Designing classes with lots of processing

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
