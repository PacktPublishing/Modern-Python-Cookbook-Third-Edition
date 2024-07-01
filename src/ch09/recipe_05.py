# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Summarizing a collection -- how to reduce


# subsection: How to do it...

from functools import reduce
from collections.abc import Iterable

def mul(a: int, b: int) -> int:
    return a * b

def prod(values: Iterable[int]) -> int:
    return reduce(mul, values, 1)

def factorial(n: int) -> int:
    return prod(range(1, n+1))

test_example_1_5 = """
>>> factorial(52)
80658175170943878571660636856403766975289505440883277824000000000000
"""

test_example_1_6 = """
>>> factorial(52) // (factorial(6) * factorial(52 - 6))
20358520
"""

# subsection: How it works...

from collections.abc import Callable
from typing import TypeVar, cast

T = TypeVar("T")

def my_reduce(
    fn: Callable[[T, T], T],
    source: Iterable[T],
    initial: T | None = None
) -> T:
    result: T = initial if initial is not None else cast(T, 0)
    for item in source:
        result = fn(result, item)
    return result

# subsection: There's more...

def imul(a: int, b: int) -> int:
    return a * b

lmul: Callable[[int, int], int] = lambda a, b: a * b

# subsection: There's more...
# Topic: Maxima and minima

def my_max(source: Iterable[T]) -> T:
    src_iter = iter(source)
    try:
        base = next(src_iter)
        max_rule = lambda a, b: a if a > b else b
        return reduce(max_rule, src_iter, base)
    except StopIteration:
        raise ValueError(f'my_max() iterable argument is empty')


# End of Summarizing a collection -- how to reduce

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
