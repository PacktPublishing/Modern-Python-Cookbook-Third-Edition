# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Refactoring a .csv DictReader as a dataclass reader (Bonus)


# Subection: Getting ready

example_data = """
lat,lon,date,time
32.8321666666667,-79.9338333333333,2012-11-27,09:15:00
31.6714833333333,-80.93325,2012-11-28,00:00:00
30.7171666666667,-81.5525,2012-11-28,11:35:00
"""

from pathlib import Path

def get_waypoints_raw(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            print(row)

# Subection: How to do it...

from dataclasses import dataclass, field
import csv
@dataclass
class Waypoint:
    arrival_date: str
    arrival_time: str
    lat: str
    lon: str


from collections.abc import Iterator

def read_data(source: Path) -> Iterator[Waypoint]:
    with source.open() as source_file:
        drdr = csv.DictReader(source_file)
        for row in drdr:
            yield Waypoint(
                arrival_date=row['date'],
                arrival_time=row['time'],
                lat=row['lat'],
                lon=row['lon']
            )

import datetime

@dataclass
class Waypoint_1:
    arrival_date: str
    arrival_time: str
    lat: str
    lon: str
    arrival_timestamp: datetime.datetime

    @classmethod
    def from_csv(cls, row: dict[str, str]) -> "Waypoint_1":
        ts_date = datetime.datetime.strptime(
            row['arrival_date'], "%Y-%m-%d"
        ).date()
        ts_time = datetime.datetime.strptime(
            row['arrival_time'], "%H:%M:%S"
        ).time()
        timestamp = datetime.datetime.combine(
            ts_date, ts_time
        )
        return Waypoint_1(
            arrival_date=row['arrival_date'],
            arrival_time=row['arrival_time'],
            lat=row['lat'],
            lon=row['lon'],
            arrival_timestamp=timestamp
        )

    @property
    def lat_lon(self) -> tuple[float, float]:
        return float(self.lat), float(self.lon)

def show_waypoints_1(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        waypoint_iter = (
            Waypoint_1.from_csv(row)
            for row in data_reader
        )

        for row in waypoint_iter:
            print(
                f"{row.arrival_timestamp:%m-%d %H:%M}, "
                f"{row.lat_lon[0]:.3f} "
                f"{row.lat_lon[1]:.3f}"
            )

@dataclass
class Waypoint_2:
    raw_data: dict[str, str]
    arrival_timestamp: datetime.datetime
    lat: float
    lon: float

    @classmethod
    def from_csv(cls, row: dict[str, str]) -> 'Waypoint_2 | None':
        try:
            ts_date = datetime.datetime.strptime(
                row['date'], "%Y-%m-%d"
            ).date()
            ts_time = datetime.datetime.strptime(
                row['time'], "%H:%M:%S"
            ).time()
            arrival = datetime.datetime.combine(
                ts_date, ts_time)
            return Waypoint_2(
                raw_data=row,
                arrival_timestamp=arrival,
                lat=float(row['lat']),
                lon=float(row['lon'])
            )
        except (ValueError, KeyError):
            return None

    @property
    def lat_lon(self) -> tuple[float, float]:
        return self.lat, self.lon


def show_waypoints_2(data_path: Path) -> None:
    with data_path.open() as data_file:
        data_reader = csv.DictReader(data_file)
        waypoint_iter = (
            Waypoint_2.from_csv(row)
            for row in data_reader
        )
        for row in filter(None, waypoint_iter):
            print(
                f"{row.arrival_timestamp:%m-%d %H:%M}, "
                f"{row.lat_lon[0]:.3f} "
                f"{row.lat_lon[1]:.3f=}"
            )


# End of Refactoring a .csv DictReader as a dataclass reader

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
