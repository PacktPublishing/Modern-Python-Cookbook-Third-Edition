# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Managing multiple contexts with multiple resources


# Subection: Getting ready

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    lat: float
    lon: float

from dataclasses import dataclass, field

@dataclass
class Leg:
    start: Point
    end: Point
    distance: float = field(init=False)

from distance_computation import NM, MI, KM, haversine

from types import TracebackType

class LegMaker:
    def __init__(self, r: float=NM) -> None:
        self.last_point: Point | None = None
        self.last_leg: Leg | None = None
        self.r = r

    def __enter__(self) -> "LegMaker":
        return self

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None
    ) -> bool | None:
        return None

    def waypoint(self, next_point: Point) -> Leg | None:
        leg: Leg | None
        if self.last_point is None:
            # Special case for the first leg
            self.last_point = next_point
            leg = None
        else:
            leg = Leg(self.last_point, next_point)
            d = haversine(
                leg.start.lat, leg.start.lon,
                leg.end.lat, leg.end.lon,
                R=self.r
            )
            leg.distance = round(d)
            self.last_point = next_point
        return leg

# Subection: How to do it...

HEADERS = ["start_lat", "start_lon", "end_lat", "end_lon", "distance"]

from collections.abc import Iterable
import csv
from dataclasses import asdict
from pathlib import Path

def flat_dict(leg: Leg) -> dict[str, float]:
    struct = asdict(leg)
    return dict(
        start_lat=struct["start"]["lat"],
        start_lon=struct["start"]["lon"],
        end_lat=struct["end"]["lat"],
        end_lon=struct["end"]["lon"],
        distance=struct["distance"],
    )

def make_route_file(
    points: Iterable[Point], target: Path
) -> None:
    with (
        LegMaker(r=NM) as legger,
        target.open('w', newline='') as csv_file
    ):
        writer = csv.DictWriter(csv_file, HEADERS)
        writer.writeheader()
        for point in points:
            leg = legger.waypoint(point)
            if leg is not None:
                writer.writerow(flat_dict(leg))
        print(f"Finished creating {target}")

# Subection: There's more...

import bz2

def make_route_bz2(points: Iterable[Point], target: Path) -> None:
    with (
        LegMaker(r=NM) as legger,
        bz2.open(target, "wt") as archive
    ):
        writer = csv.DictWriter(archive, HEADERS)
        writer.writeheader()
        for point in points:
            leg = legger.waypoint(point)
            if leg is not None:
                writer.writerow(flat_dict(leg))
    print(f"Finished creating {target}")


# End of Managing multiple contexts with multiple resources

test_make_route_file = """
>>> target = Path.cwd() / "data" / "route.tmp"
>>> points = [
...     Point(38.9928, -76.4513),
...     Point(38.3312, -76.4592),
...     Point(37.8404, -76.2742),
... ]
>>> make_route_file(points, target)
Finished creating .../data/route.tmp
>>> actual = target.read_text()
>>> from pprint import pprint
>>> pprint(actual.splitlines())
['start_lat,start_lon,end_lat,end_lon,distance',
 '38.9928,-76.4513,38.3312,-76.4592,40',
 '38.3312,-76.4592,37.8404,-76.2742,31']
"""

test_make_route_bz2 = """
>>> target = Path.cwd() / "data" / "route.tmp"
>>> points = [
...     Point(38.9928, -76.4513),
...     Point(38.3312, -76.4592),
...     Point(37.8404, -76.2742),
... ]
>>> make_route_bz2(points, target)
Finished creating .../data/route.tmp
>>> import bz2
>>> actual = bz2.open(target).read().decode('utf-8')
>>> from pprint import pprint
>>> pprint(actual.splitlines())
['start_lat,start_lon,end_lat,end_lon,distance',
 '38.9928,-76.4513,38.3312,-76.4592,40',
 '38.3312,-76.4592,37.8404,-76.2742,31']
"""

test_context_residue = """
>>> with LegMaker(r=NM) as legger:
...     legger.waypoint(Point(38.9928, -76.4513))
...     legger.waypoint(Point(38.3312, -76.4592))
Leg(start=Point(lat=38.9928, lon=-76.4513), end=Point(lat=38.3312, lon=-76.4592), distance=40)
>>> legger.waypoint(Point(37.8404, -76.2742))
Leg(start=Point(lat=38.3312, lon=-76.4592), end=Point(lat=37.8404, lon=-76.2742), distance=31)
"""

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}

