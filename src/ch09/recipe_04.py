# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Picking a subset -- three ways to filter

from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")

def should_be_passed(item: T) -> bool:
    return True  # Some function of T.

def data_filter_iter(
    source: Iterable[T]
) -> Iterator[T]:
    for item in source:
        if should_be_passed(item):
            yield item

# subsection: Getting ready...


test_example_2_1 = """
>>> from recipe_03 import row_merge, skip_header_date
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> data = list(tail_gen)

>>> from pprint import pprint
>>> pprint(data)
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

# subsection: How to do it...

from recipe_03 import CombinedRow

def pass_non_date(row: CombinedRow) -> bool:
    return row.date != "date"

def skip_header_date_iter(
    source: Iterable[CombinedRow]
) -> Iterator[CombinedRow]:
    for item in source:
        if pass_non_date(item):
            yield item

test_example_3_1 = """
>>> from recipe_03 import row_merge
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date_iter(row_gen)
>>> data = list(tail_gen)

>>> from pprint import pprint
>>> pprint(data)
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

# subsection: How to do it...
# Topic: Using a filter in a generator expression

extract_3_2 = """
(item
for item in source
if pass_module (item))
"""

def skip_header_gen(
    source: Iterable[CombinedRow]
) -> Iterator[CombinedRow]:
    return (
        item
        for item in source
        if pass_non_date(item)
    )

test_example_3_2 = """
>>> from recipe_03 import row_merge
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_gen(row_gen)
>>> data = list(tail_gen)

>>> from pprint import pprint
>>> pprint(data)
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

# subsection: How to do it...
# Topic: Using the filter() function

extract_3_3 = """
filter(pass_non_date, row_gen)
"""

test_example_3_3 = """
>>> from recipe_03 import row_merge
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = filter(pass_non_date, row_gen)
>>> data = list(tail_gen)

>>> from pprint import pprint
>>> pprint(data)
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""


# subsection: How it works...

from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

P = TypeVar("P")

def my_filter_stmt(
    f: Callable[[P], bool], source: Iterable[P]
) -> Iterator[P]:
    for item in source:
        if f(item):
            yield item

def my_filter_gen(
    f: Callable[[P], bool], source: Iterable[P]
) -> Iterator[P]:
    return (
        item
        for item in source
        if f(item)
    )

# subsection: There's more...

import datetime

def row_has_date(row: CombinedRow) -> bool:
    try:
        datetime.datetime.strptime(row.date, "%m/%d/%y")
        return True
    except ValueError as ex:
        return False

def pass_date_iter(
    source: Iterable[CombinedRow]
) -> Iterator[CombinedRow]:
    for item in source:
        if row_has_date(item):
            yield item

test_example_6_3 = """
>>> from recipe_03 import row_merge
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = pass_date_iter(row_gen)
>>> data = list(tail_gen)

>>> from pprint import pprint
>>> pprint(data)
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

# End of Picking a subset -- three ways to filter

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
