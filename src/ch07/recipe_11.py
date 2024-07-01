# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Creating contexts and context managers


# Subection: Getting ready


test_example_1_1 = """
>>> p1 = Point(38.9928, -76.4513)
>>> p2 = Point(38.3312, -76.4592)
>>> p3 = Point(37.8404, -76.2742)
>>> with Distance(r=NM) as nm_dist:
...     print(f"{nm_dist(p1, p2)=:.2f}")
...     print(f"{nm_dist(p2, p3)=:.2f}")
nm_dist(p1, p2)=39.72
nm_dist(p2, p3)=30.74
"""

# Subection: How to do it...

from collections.abc import Callable
from types import TracebackType
from typing import NamedTuple


class Point(NamedTuple):
    lat: float
    lon: float

from distance_computation import NM, MI, KM, haversine

class Distance:
    def __init__(self, r: float) -> None:
        self.r = r

    def __enter__(self) -> Callable[[Point, Point], float]:
        return self.distance

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None
    ) -> bool | None:
        return None

    def distance(self, p1: Point, p2: Point) -> float:
        return haversine(
            p1.lat, p1.lon, p2.lat, p2.lon, R=self.r
        )


# Subection: How it works...


test_example_3_1 = """
>>> p1 = Point(38.9784, -76.4922)
>>> p2 = Point(36.8443, -76.2922)
>>> nm_distance = Distance(r=NM)
>>> with nm_distance as nm_calc:
...     print(f"{nm_calc(p1, p2)=:.2f}")
nm_calc(p1, p2)=128.48
"""

# Subection: There's more\ldots

class Snippet_4_1:
    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None
    ) -> bool | None:
        # Cleanup goes here.
        return None

test_example_4_2 = """
>>> p1 = Point(38.9784, -76.4922)
>>> p2 = Point(36.8443, -76.2922)
>>> with Distance(None) as nm_dist:
...     print(f"{nm_dist(p1, p2)=:.2f}")
Traceback (most recent call last):
...
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
"""

class Distance_2:
    def __init__(self, r: float) -> None:
        self.r = r

    def __enter__(self) -> Callable[[Point, Point], float]:
        return self.distance

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None
    ) -> bool | None:
        if exc_type is TypeError:
            raise ValueError(f"Invalid r={self.r!r}")
        return None

    def distance(self, p1: Point, p2: Point) -> float:
        return haversine(p1.lat, p1.lon, p2.lat, p2.lon, R=self.r)


# End of Creating contexts and context managers

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
