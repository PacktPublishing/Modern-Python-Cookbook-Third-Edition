# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Using stacked generator expressions


# subsection: Getting ready


test_example_1_1 = """
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)
>>> log_rows[0]
['date', 'engine on', 'fuel height']

>>> log_rows[-1]
['', "choppy -- anchor in jackson's creek", '']
"""

test_example_1_2 = """
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)
>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> datetime_gen = (convert_datetime(row) for row in tail_gen)

>>> total_time = datetime.timedelta(0)
>>> total_fuel = 0
>>> for row in datetime_gen:
...     total_time += row.engine_off - row.engine_on
...     total_fuel += (
...         float(row.engine_on_fuel_height) -
...         float(row.engine_off_fuel_height)
... )

>>> print(
... f"{total_time.total_seconds()/60/60 = :.2f}, "
... f"{total_fuel = :.2f}")
total_time.total_seconds()/60/60 = 14.07, total_fuel = 7.00

"""

# subsection: How to do it...
# Topic: Restructuring the rows

from typing import NamedTuple

class CombinedRow(NamedTuple):
    # Line 1
    date: str
    engine_on_time: str
    engine_on_fuel_height: str
    # Line 2
    filler_1: str
    engine_off_time: str
    engine_off_fuel_height: str
    # Line 3
    filler_2: str
    other_notes: str
    filler_3: str

from typing import TypeAlias
from collections.abc import Iterable, Iterator

RawRow: TypeAlias = list[str]

def row_merge(
    source: Iterable[RawRow]
) -> Iterator[CombinedRow]:
    cluster: RawRow = []
    for row in source:
        if all(len(col) == 0 for col in row):
            continue
        elif len(row[0]) != 0:
            # Non-empty column 1: line 1
            if len(cluster) == 9:
                yield CombinedRow(*cluster)
            cluster = row.copy()
        else:
            # Empty column 1: line 2 or line 3
            cluster.extend(row)
    if len(cluster) == 9:
        yield CombinedRow(*cluster)


test_example_2_4 = """
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> from pprint import pprint
>>> pprint(list(row_merge(log_rows)))
[CombinedRow(date='date', engine_on_time='engine on', engine_on_fuel_height='fuel height', filler_1='', engine_off_time='engine off', engine_off_fuel_height='fuel height', filler_2='', other_notes='Other notes', filler_3=''),
 CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]

"""

# subsection: How to do it...
# Topic: Excluding the header row

def skip_header_date(
    source: Iterable[CombinedRow]
) -> Iterator[CombinedRow]:
  for row in source:
    if row.date == "date":
        continue
    yield row

test_example_3_4 = """
>>> from pprint import pprint
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)

>>> pprint(list(tail_gen))
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

# subsection: How to do it...
# Topic: Creating more useful row objects

import datetime
from typing import NamedTuple

class DatetimeRow(NamedTuple):
    date: datetime.date
    engine_on: datetime.datetime
    engine_on_fuel_height: str
    engine_off: datetime.datetime
    engine_off_fuel_height: str
    other_notes: str

def convert_datetime(row: CombinedRow) -> DatetimeRow:
    travel_date = datetime.datetime.strptime(
        row.date, "%m/%d/%y").date()
    start_time = datetime.datetime.strptime(
        row.engine_on_time, "%I:%M:%S %p").time()
    start_datetime = datetime.datetime.combine(
        travel_date, start_time)
    end_time = datetime.datetime.strptime(
        row.engine_off_time, "%I:%M:%S %p").time()
    end_datetime = datetime.datetime.combine(
        travel_date, end_time)

    return DatetimeRow(
        date=travel_date,
        engine_on=start_datetime,
        engine_off=end_datetime,
        engine_on_fuel_height=row.engine_on_fuel_height,
        engine_off_fuel_height=row.engine_off_fuel_height,
        other_notes=row.other_notes
    )

test_example_4_4 = """
>>> from pprint import pprint
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> datetime_gen = (convert_datetime(row) for row in tail_gen)

>>> pprint(list(datetime_gen))
[DatetimeRow(date=datetime.date(2013, 10, 25), engine_on=datetime.datetime(2013, 10, 25, 8, 24), engine_on_fuel_height='29', engine_off=datetime.datetime(2013, 10, 25, 13, 15), engine_off_fuel_height='27', other_notes="calm seas -- anchor solomon's island"),
 DatetimeRow(date=datetime.date(2013, 10, 26), engine_on=datetime.datetime(2013, 10, 26, 9, 12), engine_on_fuel_height='27', engine_off=datetime.datetime(2013, 10, 26, 18, 25), engine_off_fuel_height='22', other_notes="choppy -- anchor in jackson's creek")]
"""

# subsection: How it works...


test_example_5_1 = """
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> datetime_gen = (convert_datetime(row) for row in tail_gen)
>>> for row in datetime_gen:
...     print(f"{row.date}: duration {row.engine_off-row.engine_on}")
2013-10-25: duration 4:51:00
2013-10-26: duration 9:13:00
"""

# subsection: There's more...

class DurationRow(NamedTuple):
    date: datetime.date
    engine_on: datetime.datetime
    engine_on_fuel_height: str
    engine_off: datetime.datetime
    engine_off_fuel_height: str
    duration: float
    other_notes: str


def duration(row: DatetimeRow) -> DurationRow:
    travel_hours = round(
        (row.engine_off - row.engine_on)
        .total_seconds() / 60 / 60,
        1
    )
    return DurationRow(
        date=row.date,
        engine_on=row.engine_on,
        engine_off=row.engine_off,
        engine_on_fuel_height=row.engine_on_fuel_height,
        engine_off_fuel_height=row.engine_off_fuel_height,
        other_notes=row.other_notes,
        duration=travel_hours
    )


class Leg(NamedTuple):
    date: datetime.date
    engine_on: datetime.datetime
    engine_on_fuel_height: float
    engine_off: datetime.datetime
    engine_off_fuel_height: float
    duration: float
    other_notes: str


def convert_height(row: DurationRow) -> Leg:
    return Leg(
        date=row.date,
        engine_on=row.engine_on,
        engine_off=row.engine_off,
        duration=row.duration,
        engine_on_fuel_height=
            float(row.engine_on_fuel_height),
        engine_off_fuel_height=
            float(row.engine_off_fuel_height),
        other_notes=row.other_notes
    )


def leg_duration_iter(
    source: Iterable[list[str]]
) -> Iterator[Leg]:
    merged_rows = row_merge(source)
    tail_gen = skip_header_date(merged_rows)
    datetime_gen = (convert_datetime(row) for row in tail_gen)
    duration_gen = (duration(row) for row in datetime_gen)
    height_gen = (convert_height(row) for row in duration_gen)
    return height_gen


test_example_6_6 = """
>>> from pprint import pprint
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)
...     durations = leg_duration_iter(log_rows)
>>> pprint(list(durations))
[Leg(date=datetime.date(2013, 10, 25), engine_on=datetime.datetime(2013, 10, 25, 8, 24), engine_on_fuel_height=29.0, engine_off=datetime.datetime(2013, 10, 25, 13, 15), engine_off_fuel_height=27.0, duration=4.8, other_notes="calm seas -- anchor solomon's island"),
 Leg(date=datetime.date(2013, 10, 26), engine_on=datetime.datetime(2013, 10, 26, 9, 12), engine_on_fuel_height=27.0, engine_off=datetime.datetime(2013, 10, 26, 18, 25), engine_off_fuel_height=22.0, duration=9.2, other_notes="choppy -- anchor in jackson's creek")]
"""

# End of Using stacked generator expressions

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
