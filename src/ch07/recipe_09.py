# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Extending a built-in collection -- a list that does statistics


# Subection: How to do it...

import math

class StatsList(list[float]):
    def sum(self) -> float:
        return sum(v for v in self)
    def size(self) -> float:
        return sum(1 for v in self)
    def mean(self) -> float:
        return self.sum() / self.size()
    def sum2(self) -> float:
        return sum(v ** 2 for v in self)
    def variance(self) -> float:
        return (
          (self.sum2() - self.sum() ** 2 / self.size())
          / (self.size() - 1)
        )
    def stddev(self) -> float:
        return math.sqrt(self.variance())

test_example_1_6 = """
>>> subset1 = StatsList([10, 8, 13, 9, 11])
>>> data = StatsList([14, 6, 4, 12, 7, 5])
>>> data.extend(subset1)

>>> data
[14, 6, 4, 12, 7, 5, 10, 8, 13, 9, 11]

>>> data.mean()
9.0
>>> data.variance()
11.0
"""

# Subection: There's more...

from collections.abc import MutableMapping

class MyFancyMapping(MutableMapping[int, int]):
    ... # etc.


# End of Extending a built-in collection -- a list that does statistics

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
