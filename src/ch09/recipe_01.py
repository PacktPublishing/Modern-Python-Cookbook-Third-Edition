# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Writing generator functions with the yield statement


from typing import cast

from collections.abc import Iterable, Iterator

class P: ...
class Q: ...

def some_iter(source: Iterable[P]) -> Iterator[Q]:
    ...  # Using yield

    yield cast(Q, None)

# subsection: Getting ready

data = """
[2016-06-15 17:57:54,715] INFO in ch10_r10: Sample Message One
[2016-06-15 17:57:54,716] DEBUG in ch10_r10: Debugging
[2016-06-15 17:57:54,720] WARNING in ch10_r10: Something might have gone wrong
"""

import re

pattern = re.compile(
    r"\[(?P<date>.*?)\]\s+"
    r"(?P<level>\w+)\s+"
    r"in\s+(?P<module>.+?)"
    r":\s+(?P<message>.+)",
    re.X
)


from typing import NamedTuple

class RawLog(NamedTuple):
    date: str
    level: str
    module: str
    message: str

test_example_1_5 = """ 
RawLog(date='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One')
"""

# subsection: How to do it...

import re
from collections.abc import Iterable, Iterator

def parse_line_iter(
    source: Iterable[str]
) -> Iterator[RawLog]:
    pattern = re.compile(
        r"\[(?P<date>.*?)\]\s+"
        r"(?P<level>\w+)\s+"
        r"in\s+(?P<module>.+?)"
        r":\s+(?P<message>.+)",
        re.X
    )
    for line in source:
        if match := pattern.match(line):
            yield RawLog(*match.groups())

test_example_3_6 = """
>>> log_lines = [
... '[2016-04-24 11:05:01,462] INFO in module1: Sample Message One',
... '[2016-04-24 11:06:02,624] DEBUG in module2: Debugging',
... '[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong'
... ]

>>> from pprint import pprint

>>> for item in parse_line_iter(log_lines):
...     pprint(item)
RawLog(date='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One')
RawLog(date='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')
RawLog(date='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')


>>> details = list(parse_line_iter(log_lines))
>>> details
[RawLog(date='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'), RawLog(date='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging'), RawLog(date='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')]

>>> parse_line_iter(data)
<generator object parse_line_iter at ...>
"""

# subsection: How it works...

test_example_4_1 = """
>>> some_collection = ["hello", "world"]
>>> def process(item) -> None:
...     print(item)

>>> for i in some_collection:
...     process(i)
hello
world

>>> the_iterator = iter(some_collection)
>>> try:
...     while True:
...         i = next(the_iterator)
...         process(i)
... except StopIteration:
...     pass
hello
world

"""

test_example_4_3 = """
>>> def gen_func():
...     print("pre-yield")
...     yield 1
...     print("post-yield")
...     yield 2

>>> y = gen_func()
>>> next(y)
pre-yield
1

>>> next(y)
post-yield
2

>>> next(y)
Traceback (most recent call last):
...
StopIteration
"""

# subsection: There's more...

import datetime
from typing import NamedTuple

class DatedLog(NamedTuple):
    date: datetime.datetime
    level: str
    module: str
    message: str

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

test_example_5_3 = """
>>> from textwrap import wrap
>>> line_break = lambda thing: '\\n'.join(wrap(str(thing), subsequent_indent=' '))
>>> log_lines = [
... '[2016-04-24 11:05:01,462] INFO in module1: Sample Message One',
... '[2016-04-24 11:06:02,624] DEBUG in module2: Debugging',
... '[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong'
... ]

# Code example without formatting clutter.
>>> for item in parse_date_iter(parse_line_iter(log_lines)):
...     print(item)
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000), level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000), level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000), level='WARNING', module='module1', message='Something might have gone wrong')

# Code example with formatting clutter.
>>> for item in parse_date_iter(parse_line_iter(log_lines)):
...     print(line_break(item))
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 5, 1, 462000),
 level='INFO', module='module1', message='Sample Message One')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 6, 2, 624000),
 level='DEBUG', module='module2', message='Debugging')
DatedLog(date=datetime.datetime(2016, 4, 24, 11, 7, 3, 246000),
 level='WARNING', module='module1', message='Something might have gone
 wrong')
"""


# End of Writing generator functions with the yield statement

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
