# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Managing global and singleton objects


# Subection: Getting ready

code_snippet_1_1 = """
for row in source:
    count('input')
    some_processing()
print(counts())
"""

# Subection: How to do it...
# Topic: Global module variables

from collections import Counter

_global_counter: Counter[str] = Counter()

def count(key: str, increment: int = 1) -> None:
    _global_counter[key] += increment

def counts() -> list[tuple[str, int]]:
    return _global_counter.most_common()

test_example_2_4 = """
>>> from counter import *
>>> from recipe_03 import Dice1

>>> d = Dice1(1)
>>> for _ in range(1000):
...     if sum(d.roll()) == 7: 
...         count('seven')
...     else: 
...         count('other')
>>> print(counts())
[('other', 833), ('seven', 167)]
"""

# Subection: How to do it...
# Topic: Class-level "static" variables

from collections import Counter
from typing import ClassVar

class EventCounter:

    _class_counter: ClassVar[Counter[str]] = Counter()

    @classmethod
    def count(cls, key: str, increment: int = 1) -> None:
        cls._class_counter[key] += increment

    @classmethod
    def counts(cls) -> list[tuple[str, int]]:
        return cls._class_counter.most_common()

test_example_3_3 = """
>>> from counter import *
>>> EventCounter.count('input')

>>> EventCounter.count('input')
>>> EventCounter.count('filter')

>>> EventCounter.counts()
[('input', 2), ('filter', 1)]
"""


# End of Managing global and singleton objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
