# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Implementing ``there exists'' processing


# subsection: How to do it...


from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")

def find_first(
    fn:  Callable[[T], bool], source: Iterable[T]
) -> Iterator[T]:
    for item in source:
        if fn(item):
            yield item
            break

test_example_1_2 = """
>>> n = 15
>>> lambda i: n % i == 0
<function <lambda> at ...>

>>> (lambda i: n % i == 0)(5)
True
"""

import math

def prime(n: int) -> bool:
    factors = find_first(
        lambda i: n % i == 0,
        range(2, int(math.sqrt(n) + 1)) )
    return len(list(factors)) == 0

# subsection: There's more...



test_example_2_1 = """
>>> from itertools import takewhile

>>> n = 47
>>> list(takewhile(lambda i: n % i != 0, range(2, 8)))
[2, 3, 4, 5, 6, 7]

>>> n = 49
>>> list(takewhile(lambda i: n % i != 0, range(2, 8)))
[2, 3, 4, 5, 6]
"""

from itertools import takewhile

def prime_t(n: int) -> bool:
    tests = set(range(2, int(math.sqrt(n) + 1)))
    non_factors = set(takewhile(lambda i: n % i != 0, tests))
    return tests == non_factors

def prime_any(n: int) -> bool:
    tests = range(2, int(math.sqrt(n) + 1))
    has_factors = any(n % t == 0 for t in tests)
    return not has_factors


# End of Implementing ``there exists'' processing

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
