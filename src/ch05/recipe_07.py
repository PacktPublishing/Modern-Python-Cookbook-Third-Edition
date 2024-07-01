# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Avoiding mutable default values for function parameters


# Subsection: Getting ready

from collections import Counter
from random import randint, seed

def gather_stats_bad(
    n: int,
    samples: int = 1000,
    summary: Counter[int] = Counter()
) -> Counter[int]:
    summary.update(
      sum(randint(1, 6)
      for d in range(n)) for _ in range(samples)
    )
    return summary


test_example_1_2 = """
>>> seed(1)
>>> s1 = gather_stats_bad(2)
>>> s1
Counter({7: 168, 6: 147, 8: 136, 9: 114, 5: 110, 10: 77, 11: 71, 4: 70, 3: 52, 12: 29, 2: 26})


>>> seed(1)
>>> mc = Counter()
>>> gather_stats_bad(2, summary=mc)
Counter...
>>> mc
Counter({7: 168, 6: 147, 8: 136, 9: 114, 5: 110, 10: 77, 11: 71, 4: 70, 3: 52, 12: 29, 2: 26})


>>> seed(1)
>>> s3b = gather_stats_bad(2)
>>> s3b
Counter({7: 336, 6: 294, 8: 272, 9: 228, 5: 220, 10: 154, 11: 142, 4: 140, 3: 104, 12: 58, 2: 52})

>>> s1 is s3b
True
"""

# Subsection: How to do it...

def gather_stats_good(
    n: int,
    summary: Counter[int] | None = None,
    samples: int = 1000,
) -> Counter[int]:
    if summary is None:
        summary = Counter()
    summary.update(
      sum(randint(1, 6)
      for d in range(n)) for _ in range(samples)
    )
    return summary

# Subsection: How it works...

def update_stats(
    n: int,
    summary: Counter[int],
    samples: int = 1000,
) -> Counter[int]:
    summary.update(
        sum(randint(1, 6)
        for d in range(n)) for _ in range(samples))
    return summary

def create_stats(n: int, samples: int = 1000) -> Counter[int]:
    return update_stats(n, Counter(), samples)


# Subsection: There's more...

from collections import Counter
from collections.abc import Callable, Iterable, Hashable
from typing import TypeVar, TypeAlias

T = TypeVar('T', bound=Hashable)
Summarizer: TypeAlias = Callable[[Iterable[T]], Counter[T]]

def gather_stats_flex(
    n: int,
    samples: int = 1000,
    summary_func: Summarizer[int] = Counter
) -> Counter[int]:
    summary = summary_func(
        sum(randint(1, 6)
        for d in range(n)) for _ in range(samples))
    return summary


test_flex = """
>>> seed(1)
>>> gather_stats_flex(2, 12, summary_func=list)
[7, 4, 5, 8, 10, 3, 5, 8, 6, 10, 9, 7]

>>> seed(1)
>>> gather_stats_flex(2, 12, summary_func=list)
[7, 4, 5, 8, 10, 3, 5, 8, 6, 10, 9, 7]
"""


test_example_4_3 = """
>>> seed(1)
>>> gather_stats_flex(2, 12)
Counter({7: 2, 5: 2, 8: 2, 10: 2, 4: 1, 3: 1, 6: 1, 9: 1})
"""


# End of Avoiding mutable default values for function parameters

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
