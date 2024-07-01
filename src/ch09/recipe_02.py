# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Applying transformations to a collection

from collections.abc import Iterable, Iterator
from typing import TypeVar, cast

class X: ...
class Y: ...

def some_transformation(x: X) -> Y:
    pass

    return cast(Y, None)

def new_item_iter(source: Iterable[X]) -> Iterator[Y]:
    for item in source:
        new_item: Y = some_transformation(item)
        yield new_item

# subsection: Getting ready...


test_example_2_1 = """
>>> data = [
... RawLog("2016-04-24 11:05:01,462", "INFO", "module1", "Sample Message One"),
... RawLog("2016-04-24 11:06:02,624", "DEBUG", "module2", "Debugging"),
... RawLog("2016-04-24 11:07:03,246", "WARNING", "module1", "Something might have gone wrong"),
... ]
"""



import datetime
from recipe_01 import RawLog, DatedLog

def parse_date_iter(
    source: Iterable[RawLog]
) -> Iterator[DatedLog]:
    for item in source:
        date = datetime.datetime.strptime(
            item.date, "%Y-%m-%d %H:%M:%S,%f"
        )
        yield DatedLog(
            date, item.level, item.module, item.message
        )

# subsection: How to do it...

def parse_date(item: RawLog) -> DatedLog:
    date = datetime.datetime.strptime(
        item.date, "%Y-%m-%d %H:%M:%S,%f")
    return DatedLog(
        date, item.level, item.module, item.message)

test_example_3_2 = """
>>> item = RawLog("2016-04-24 11:05:01,462", "INFO", "module1", "Sample Message One")
>>> parse_date(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
"""

# subsection: How to do it...
# Topic: Using a for statement

def parse_date_iter_y(
    source: Iterable[RawLog]
) -> Iterator[DatedLog]:
    for item in source:
        yield parse_date(item)

# subsection: How to do it...
# Topic: Using a generator expression

test_example_4_2 = """
>>> source = []
>>> for item in source:
...     parse_date(item)
"""

def parse_date_iter_g(
    source: Iterable[RawLog]
) -> Iterator[DatedLog]:
  return (parse_date(item) for item in source)

# subsection: How to do it...
# Topic: Using the map() function


test_example_4_3 = """
>>> source = []
>>> map(parse_date, source)
<map object at ...>
"""

def parse_date_iter_m(
    source: Iterable[RawLog]
) -> Iterator[DatedLog]:
    return map(parse_date, source)

# subsection: How it works...

from typing import TypeVar
from collections.abc import Callable, Iterable, Iterator

P = TypeVar("P")
Q = TypeVar("Q")

def my_map1(f: Callable[[P], Q], source: Iterable[P]) -> Iterator[Q]:
    for item in source:
        yield f(item)

def my_map2(f: Callable[[P], Q], source: Iterable[P]) -> Iterator[Q]:
    return (f(item) for item in source)

# subsection: There's more...


test_example_8_1 = """
>>> def mul(a, b):
...     return a * b

>>> list_1 = [2, 3, 5, 7]
>>> list_2 = [11, 13, 17, 23]

>>> list(map(mul, list_1, list_2))
[22, 39, 85, 161]

>>> def bundle(*args):
...     return args

>>> list(map(bundle, list_1, list_2))
[(2, 11), (3, 13), (5, 17), (7, 23)]
"""


# End of Applying transformations to a collection

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
