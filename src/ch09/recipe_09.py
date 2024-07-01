# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Simplifying complex algorithms with immutable data structures


# Subsection: Getting ready

text_1 = """
10	8.04
8	6.95
13	7.58
9	8.81
11	8.33
14	9.96
6	7.24
4	4.26
12	10.84
7	4.82
5	5.68
"""

text_2 = """
10	9.14
8	8.14
13	8.74
9	8.77
11	9.26
14	8.1
6	6.13
4	3.1
12	9.13
7	7.26
5	4.74
"""

from typing import Iterable, Iterator


def text_parse(text: str) -> Iterator[list[str]]:
    non_empty = filter(None, text.splitlines())
    return (r.split() for r in non_empty)


from dataclasses import dataclass

@dataclass
class DataPair:
    x: float
    y: float


def cleanse(source: Iterable[list[str]]) -> Iterator[DataPair]:
    for text_item in source:
        try:
            x_amount = float(text_item[0])
            y_amount = float(text_item[1])
            yield DataPair(x_amount, y_amount)
        except Exception as ex:
            print(f"{ex} in {text_item!r}")


data_1 = [
    DataPair(x=10.0, y=8.04),
    DataPair(x=8.0, y=6.95),
    DataPair(x=13.0, y=7.58),
    DataPair(x=9.0, y=8.81),
    DataPair(x=11.0, y=8.33),
    DataPair(x=14.0, y=9.96),
    DataPair(x=6.0, y=7.24),
    DataPair(x=4.0, y=4.26),
    DataPair(x=12.0, y=10.84),
    DataPair(x=7.0, y=4.82),
    DataPair(x=5.0, y=5.68)
]

# Subsection: How to do it...

from typing import NamedTuple

class RankYDataPair(NamedTuple):
    y_rank: int
    pair: DataPair

from collections.abc import Iterable, Iterator

def rank_by_y(
      source: Iterable[DataPair]
) -> Iterator[RankYDataPair]:
    all_data = sorted(source, key=lambda pair: pair.y)
    for y_rank, pair in enumerate(all_data, start=1):
        yield RankYDataPair(y_rank, pair)

# subsection: How it works...


test_example_3_1 = """
>>> from pprint import pprint
>>> data = rank_by_y(cleanse(text_parse(text_1)))
>>> pprint(list(data))
[RankYDataPair(y_rank=1, pair=DataPair(x=4.0, y=4.26)),
 RankYDataPair(y_rank=2, pair=DataPair(x=7.0, y=4.82)),
 RankYDataPair(y_rank=3, pair=DataPair(x=5.0, y=5.68)),
 RankYDataPair(y_rank=4, pair=DataPair(x=8.0, y=6.95)),
 RankYDataPair(y_rank=5, pair=DataPair(x=6.0, y=7.24)),
 RankYDataPair(y_rank=6, pair=DataPair(x=13.0, y=7.58)),
 RankYDataPair(y_rank=7, pair=DataPair(x=10.0, y=8.04)),
 RankYDataPair(y_rank=8, pair=DataPair(x=11.0, y=8.33)),
 RankYDataPair(y_rank=9, pair=DataPair(x=9.0, y=8.81)),
 RankYDataPair(y_rank=10, pair=DataPair(x=14.0, y=9.96)),
 RankYDataPair(y_rank=11, pair=DataPair(x=12.0, y=10.84))]
"""


# subsection: There's more...

from dataclasses import dataclass, field

@dataclass
class DataPairDC:
    x: float
    y: float
    y_rank: int = field(init=False)

from typing import Iterable, Iterator

def cleanse_dc(
    source: Iterable[list[str]]
) -> Iterator[DataPairDC]:
    for text_item in source:
        try:
            x_amount = float(text_item[0])
            y_amount = float(text_item[1])
            yield DataPairDC(x=x_amount, y=y_amount)
        except Exception as ex:
            print(ex, repr(text_item))

def rank_by_y_dc(
    source: Iterable[DataPairDC]
) -> Iterable[DataPairDC]:
    all_data = sorted(source, key=lambda pair: pair.y)
    for y_rank, pair in enumerate(all_data, start=1):
        pair.y_rank = y_rank
        yield pair


# End of Simplifying complex algorithms with immutable data structures

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
