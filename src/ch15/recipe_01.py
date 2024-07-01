# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Using docstrings for testing


# Subsection: Getting ready

from math import factorial

def binom_draft(n: int, k: int) -> int:
    return factorial(n) // (factorial(k) * factorial(n - k))



from statistics import median
from collections import Counter

class Summary:
    """
    Computes summary statistics.

    >>> s = Summary()
    >>> s.add(8)
    >>> s.add(9)
    >>> s.add(9)
    >>> round(s.mean, 2)
    8.67
    >>> s.median
    9
    >>> print(str(s))
    mean = 8.67
    median = 9
    """

    def __init__(self) -> None:
        self.counts: Counter[int] = Counter()

    def __str__(self) -> str:
        return f"mean = {self.mean:.2f}\nmedian = {self.median:d}"

    def add(self, value: int) -> None:
        self.counts[value] += 1

    @property
    def mean(self) -> float:
        s0 = sum(f for v, f in self.counts.items())
        s1 = sum(v * f for v, f in self.counts.items())
        return s1 / s0

    @property
    def median(self) -> float:
        return median(self.counts.elements())

    @property
    def mode(self) -> list[tuple[int, int]]:
        return self.counts.most_common()


# Subsection: How to do it...
# Topic: Writing examples for stateless functions


def binom(n: int, k: int) -> int:
    """
    Computes the binomial coefficient.
    This shows how many combinations exist of
    *n* things taken in groups of size *k*.

    :param n: size of the universe
    :param k: size of each subset
    :returns: the number of combinations

    >>> binom(52, 5)
    2598960

    """

    return factorial(n) // (factorial(k) * factorial(n - k))


# Subsection: How to do it...
# Topic: Writing examples for stateful objects


output_example = """
(cookbook3) % python -m doctest recipe_01.py
**********************************************************************
File "/Users/slott/Documents/Writing/Python/Python Cookbook 3e/src/ch15/recipe_01.py", line 29, in recipe_01.Summary
Failed example:
    s.median
Expected:
    10
Got:
    9
**********************************************************************
1 items had failures:
   1 of   7 in recipe_01.Summary
***Test Failed*** 1 failures.
"""


# Subsection: There's more...


def binom2(n: int, k: int) -> int:
    """
    Computes the binomial coefficient.
    This shows how many combinations exist of
    *n* things taken in groups of size *k*.

    :param n: size of the universe
    :param k: size of each subset
    :returns: the number of combinations

    >>> binom(52, 5)
    2598960
    >>> binom(52, 0)
    1
    >>> binom(52, 52)
    1

    """

    return factorial(n) // (factorial(k) * factorial(n - k))


__test__ = {
    "GIVEN_binom_WHEN_0_0_THEN_1": """
        >>> binom(0, 0)
        1
        """,
    "GIVEN_binom_WHEN_52_52_THEN_1": """
        >>> binom(52, 52)
        1
        """,
}


# End of Using docstrings for testing

__test__ |= {name: code for name, code in locals().items() if name.startswith("test_")}
