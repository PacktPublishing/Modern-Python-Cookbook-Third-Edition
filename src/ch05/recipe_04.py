# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Writing dictionary-related type hints


# Subsection: Getting ready

data = """
date,engine on,fuel height on,engine off,fuel height off
10/25/13,08:24:00,29,13:15:00,27
10/26/13,09:12:00,27,18:25:00,22
10/28/13,13:21:00,22,06:25:00,14
"""

# Subsection: How to do it...

import csv
from pathlib import Path

def get_fuel_use(source_path: Path) -> list[dict[str, str]]:
    with source_path.open() as source_file:
        rdr = csv.DictReader(source_file)
        data: list[dict[str, str]] = list(rdr)
    return data

import datetime
from typing import TypedDict

class History(TypedDict):
    date: datetime.date
    start_time: datetime.time
    start_fuel: float
    end_time: datetime.time
    end_fuel: float

from collections.abc import Iterable, Iterator

def make_history(source: Iterable[dict[str, str]]) -> Iterator[History]:
    for row in source:
        yield dict(
            date=datetime.datetime.strptime(
                row['date'], "%m/%d/%y").date(),
            start_time=datetime.datetime.strptime(
                row['engine on'], '%H:%M:%S').time(),
            start_fuel=float(row['fuel height on']),
            end_time=datetime.datetime.strptime(
                row['engine off'], '%H:%M:%S').time(),
            end_fuel=float(row['fuel height off']),
        )


test_example_2_4 = """
>>> from pprint import pprint

>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = make_history(get_fuel_use(source_path))
>>> for row in fuel_use:
...     pprint(row)
{'date': datetime.date(2013, 10, 25),
 'end_fuel': 27.0,
 'end_time': datetime.time(13, 15),
 'start_fuel': 29.0,
 'start_time': datetime.time(8, 24)}
{'date': datetime.date(2013, 10, 26),
 'end_fuel': 22.0,
 'end_time': datetime.time(18, 25),
 'start_fuel': 27.0,
 'start_time': datetime.time(9, 12)}
{'date': datetime.date(2013, 10, 28),
 'end_fuel': 14.0,
 'end_time': datetime.time(6, 25),
 'start_fuel': 22.0,
 'start_time': datetime.time(13, 21)}
"""

# Subsection: How it works...







# Subsection: There's more...

from typing import TypedDict, NotRequired

class History2(TypedDict):
   date: datetime.date
   start_time: NotRequired[datetime.time]
   start_fuel: NotRequired[float]
   end_time: NotRequired[datetime.time]
   end_fuel: NotRequired[float]


from typing import NamedTuple

class HistoryT(NamedTuple):
    date: datetime.date
    start_time: datetime.time
    start_fuel: float
    end_time: datetime.time
    end_fuel: float


# End of Writing dictionary-related type hints

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
