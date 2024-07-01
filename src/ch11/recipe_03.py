# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Reading delimited files with the CSV module


# Subection: Getting ready

data = """
lat,lon,date,time
32.8321666666667,-79.9338333333333,2012-11-27,09:15:00
31.6714833333333,-80.93325,2012-11-28,00:00:00
30.7171666666667,-81.5525,2012-11-28,11:35:00
"""

# Subection: How to do it...

import csv
from pathlib import Path

def raw(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            print(row)

test_raw = """
>>> data = Path("data") / "waypoints.csv"
>>> raw(data)
{'lat': '32.8321666666667', 'lon': '-79.9338333333333', 'date': '2012-11-27', 'time': '09:15:00'}
{'lat': '31.6714833333333', 'lon': '-80.93325', 'date': '2012-11-28', 'time': '00:00:00'}
{'lat': '30.7171666666667', 'lon': '-81.5525', 'date': '2012-11-28', 'time': '11:35:00'}
"""


# Subection: How it works...

data_2 = '''
lan,lon,date,time,notes
32.832,-79.934,2012-11-27,09:15:00,"breezy, rainy"
31.671,-80.933,2012-11-28,00:00:00,"blowing ""like stink"""
'''

# Subection: There's more...

import datetime
from typing import TypeAlias, Any

Raw: TypeAlias = dict[str, Any]

Waypoint: TypeAlias = dict[str, Any]

def clean_row(
    source_row: Raw
) -> Waypoint:
    ts_date = datetime.datetime.strptime(
        source_row["date"], "%Y-%m-%d").date()
    ts_time = datetime.datetime.strptime(
        source_row["time"], "%H:%M:%S").time()
    return dict(
        date=source_row["date"],
        time=source_row["time"],
        lat=source_row["lat"],
        lon=source_row["lon"],
        lat_lon=(
            float(source_row["lat"]),
            float(source_row["lon"])
        ),
        ts_date=ts_date,
        ts_time=ts_time,
        timestamp = datetime.datetime.combine(
            ts_date, ts_time
        )
    )

from collections.abc import Iterator

def cleanse(reader: csv.DictReader[str]) -> Iterator[Waypoint]:
    for row in reader:
        yield clean_row(row)

from pprint import pprint

def display_clean(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        clean_data_reader = cleanse(data_reader)
        for row in clean_data_reader:
            pprint(row)

test_display_clean = """
>>> data = Path("data") / "waypoints.csv"
>>> display_clean(data)
{'date': '2012-11-27',
 'lat': '32.8321666666667',
 'lat_lon': (32.8321666666667, -79.9338333333333),
 'lon': '-79.9338333333333',
 'time': '09:15:00',
 'timestamp': datetime.datetime(2012, 11, 27, 9, 15),
 'ts_date': datetime.date(2012, 11, 27),
 'ts_time': datetime.time(9, 15)}
...
"""

from typing import TypedDict

class Raw_TD(TypedDict):
    date: str
    time: str
    lat: str
    lon: str

class Waypoint_TD(Raw_TD):
    lat_lon: tuple[float, float]
    ts_date: datetime.date
    ts_time: datetime.time
    timestamp: datetime.datetime


# End of Reading delimited files with the CSV module

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
