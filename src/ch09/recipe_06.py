# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Combining the map and reduce transformations




test_example_1_1 = """
>>> typical_iterator = iter([0, 1, 2, 3, 4])
>>> sum(typical_iterator)
10

>>> sum(typical_iterator)
0
"""

# subsection: How to do it...


test_example_2_1 = """
>>> from pathlib import Path
>>> import csv
>>> from recipe_03 import row_merge, CombinedRow

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> from pprint import pprint
>>> pprint(list(row_merge(log_rows)))
[CombinedRow(date='date', engine_on_time='engine on', engine_on_fuel_height='fuel height', filler_1='', engine_off_time='engine off', engine_off_fuel_height='fuel height', filler_2='', other_notes='Other notes', filler_3=''),
 CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]

>>> round(
...     total_fuel(clean_data_iter(row_merge(log_rows))),
...     3
... )
7.0
"""

from recipe_03 import row_merge, CombinedRow
import datetime
from dataclasses import dataclass, field

@dataclass
class Leg:
    date: str
    start_time: str
    start_fuel_height: str
    end_time: str
    end_fuel_height: str
    other_notes: str
    start_timestamp: datetime.datetime = field(init=False)
    end_timestamp: datetime.datetime = field(init=False)
    travel_hours: float = field(init=False)
    fuel_change: float = field(init=False)
    fuel_per_hour: float = field(init=False)


from collections.abc import Iterable, Iterator

def clean_data_iter(
    source: Iterable[CombinedRow]
) -> Iterator[Leg]:
    leg_iter = map(make_Leg, source)
    fitered_source = filter(reject_date_header, leg_iter)
    start_iter = map(start_datetime, fitered_source)
    end_iter = map(end_datetime, start_iter)
    delta_iter = map(duration, end_iter)
    fuel_iter = map(fuel_use, delta_iter)
    per_hour_iter = map(fuel_per_hour, fuel_iter)
    return per_hour_iter

def make_Leg(row: CombinedRow) -> Leg:
    return Leg(
        date=row.date,
        start_time=row.engine_on_time,
        start_fuel_height=row.engine_on_fuel_height,
        end_time=row.engine_off_time,
        end_fuel_height=row.engine_off_fuel_height,
        other_notes=row.other_notes,
    )

def reject_date_header(row: Leg) -> bool:
    return not (row.date == "date")

def timestamp(
    date_text: str, time_text: str
) -> datetime.datetime:
    date = datetime.datetime.strptime(
        date_text, "%m/%d/%y").date()
    time = datetime.datetime.strptime(
        time_text, "%I:%M:%S %p").time()
    timestamp = datetime.datetime.combine(
        date, time)
    return timestamp

def start_datetime(row: Leg) -> Leg:
      row.start_timestamp = timestamp(
        row.date, row.start_time)
      return row

def end_datetime(row: Leg) -> Leg:
      row.end_timestamp = timestamp(
        row.date, row.end_time)
      return row

def duration(row: Leg) -> Leg:
    travel_time = row.end_timestamp - row.start_timestamp
    row.travel_hours = round(
        travel_time.total_seconds() / 60 / 60,
        1
    )
    return row

def fuel_use(row: Leg) -> Leg:
    end_height = float(row.end_fuel_height)
    start_height = float(row.start_fuel_height)
    row.fuel_change = start_height - end_height
    return row

def fuel_per_hour(row: Leg) -> Leg:
    row.fuel_per_hour = row.fuel_change / row.travel_hours
    return row

# subsection: How it works...

from statistics import *

def avg_fuel_per_hour(source: Iterable[Leg]) -> float:
    return mean(row.fuel_per_hour for row in source)

def stdev_fuel_per_hour(source: Iterable[Leg]) -> float:
    return stdev(row.fuel_per_hour for row in source)

def total_fuel(source: Iterable[Leg]) -> float:
    return sum(row.fuel_change for row in source)

test_example_3_2 = """
>>> from pathlib import Path
>>> import csv

>>> with Path('data/fuel.csv').open() as source_file:
...     reader = csv.reader(source_file)
...     log_rows = list(reader)

>>> round(
...     avg_fuel_per_hour(clean_data_iter(row_merge(log_rows))),
...     3)
0.48
"""

# subsection: There's more...

def summary(raw_data: Iterable[list[str]]) -> None:
    data = tuple(clean_data_iter(row_merge(raw_data)))
    m = avg_fuel_per_hour(data)
    s = 2 * stdev_fuel_per_hour(data)
    print(f"Fuel use {m:.2f} ±{s:.2f}")

from itertools import tee

def summary_t(raw_data: Iterable[list[str]]) -> None:
    data1, data2 = tee(clean_data_iter(row_merge(raw_data)), 2)
    m = avg_fuel_per_hour(data1)
    s = 2 * stdev_fuel_per_hour(data2)
    print(f"Fuel use {m:.2f} ±{s:.2f}")


# End of Combining the map and reduce transformations

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
