# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Using properties for lazy attributes


# Subection: Getting ready...

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

class LazyCounterStatistics:
    def __init__(self, raw_counter: Counter[int]) -> None:
        self.raw_counter = raw_counter
    @property
    def sum(self) -> float:
        return sum(
            f * v
            for v, f in self.raw_counter.items()
        )
    @property
    def count(self) -> float:
        return sum(
            f
            for v, f in self.raw_counter.items()
        )
    @property
    def mean(self) -> float:
        return self.sum / self.count
    @property
    def sum2(self) -> float:
        return sum(
            f * v ** 2
            for v, f in self.raw_counter.items()
        )
    @property
    def variance(self) -> float:
      return (
          (self.sum2 - self.sum ** 2 / self.count) /
          (self.count - 1)
      )
    @property
    def stddev(self) -> float:
        return math.sqrt(self.variance)

test_example_2_6 = """
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

test_example_2_7 = """
>>> stats = LazyCounterStatistics(data)
>>> print(f"Mean: {stats.mean:.1f}")
Mean: 10.4
>>> print(f"Standard Deviation: {stats.stddev:.2f}")
Standard Deviation: 4.17
"""

# Subection: There's more...

from typing import cast

class CachingLazyCounterStatistics:
    def __init__(self, raw_counter: Counter[int]) -> None:
        self.raw_counter = raw_counter
        self._sum: float | None = None
        self._count: float | None = None

    @property
    def sum(self) -> float:
        if self._sum is None:
            self._sum = sum(
                f * v
                for v, f in self.raw_counter.items()
            )
        return self._sum


# End of Using properties for lazy attributes

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
