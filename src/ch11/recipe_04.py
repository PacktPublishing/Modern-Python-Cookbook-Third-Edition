# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Using dataclasses to simplify working with CSV files


# Subection: Getting ready

data = """
lat,lon,date,time
32.8321666666667,-79.9338333333333,2012-11-27,09:15:00
31.6714833333333,-80.93325,2012-11-28,00:00:00
30.7171666666667,-81.5525,2012-11-28,11:35:00
"""

# Subection: How to do it...

from dataclasses import dataclass, field
import datetime
from collections.abc import Iterator

@dataclass
class RawRow:
    date: str
    time: str
    lat: str
    lon: str

@dataclass
class Waypoint:
    raw: RawRow
    lat_lon: tuple[float, float] = field(init=False)
    ts_date: datetime.date = field(init=False)
    ts_time: datetime.time = field(init=False)
    timestamp: datetime.datetime = field(init=False)

    def __post_init__(self) -> None:
        self.ts_date = datetime.datetime.strptime(
            self.raw.date, "%Y-%m-%d"
        ).date()
        self.ts_time = datetime.datetime.strptime(
            self.raw.time, "%H:%M:%S"
        ).time()
        self.lat_lon = (
            float(self.raw.lat),
            float(self.raw.lon)
        )
        self.timestamp = datetime.datetime.combine(
            self.ts_date, self.ts_time
        )

import csv

def waypoint_iter(reader: csv.DictReader[str]) -> Iterator[Waypoint]:
    for row in reader:
        raw = RawRow(**row)
        yield Waypoint(raw)


from pathlib import Path
import csv
from pprint import pprint

def display(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for waypoint in waypoint_iter(data_reader):
            pprint(waypoint)

test_wp_class = """
>>> data_path = Path("data") / "waypoints.csv"
>>> display(data_path)
Waypoint(raw=RawRow(date='2012-11-27',
                    time='09:15:00',
                    lat='32.8321666666667',
                    lon='-79.9338333333333'),
         lat_lon=(32.8321666666667, -79.9338333333333),
         ts_date=datetime.date(2012, 11, 27),
         ts_time=datetime.time(9, 15),
         timestamp=datetime.datetime(2012, 11, 27, 9, 15))
...
"""

# Subection: There's more...

@dataclass
class RawRow_HeaderV2:
    date: str
    time: str
    lat: str
    lon: str

    @classmethod
    def from_csv(cls, csv_row: dict[str, str]) -> "RawRow_HeaderV2":
        return RawRow_HeaderV2(
            date = csv_row['Date of Travel (YYYY-MM-DD)'],
            time = csv_row['Arrival Time (HH:MM:SS)'],
            lat = csv_row['Latitude (degrees N)'],
            lon = csv_row['Logitude (degrees W)'],
        )

from typing import TypeAlias

Raw: TypeAlias = RawRow | RawRow_HeaderV2


# End of Using dataclasses to simplify working with CSV files

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
