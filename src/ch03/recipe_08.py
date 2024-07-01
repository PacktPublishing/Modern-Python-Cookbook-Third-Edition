# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Picking an order for parameters based on partial functions


# Subsection: Getting ready

from math import radians, sin, cos, sqrt, asin

MI = 3959
NM = 3440
KM = 6372

def haversine(
    lat_1: float, lon_1: float,
    lat_2: float, lon_2: float, R: float
) -> float:
    """Distance between points.
    R is Earth's radius.
    R=MI computes in miles. Default is nautical miles.

    >>> round(haversine(36.12, -86.67, 33.94, -118.40, R=6372.8), 5)
    2887.25995
    """

    Δ_lat = radians(lat_2) - radians(lat_1)
    Δ_lon = radians(lon_2) - radians(lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    a = sqrt(
        sin(Δ_lat / 2) ** 2 +
        cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2
    )
    return R * 2 * asin(a)



# Subsection: How to do it...
# Topic: Wrapping a function

def haversine_k(
    lat_1: float, lon_1: float,
    lat_2: float, lon_2: float, *, R: float
) -> float:
    ... # etc.
    return 0.0  # A placeholder for mypy

def nm_haversine_1(*args):
    return haversine_k(*args, R=NM)


# Subsection: How to do it...
# Topic: Creating a partial function with keyword parameters


from functools import partial
nm_haversine_3 = partial(haversine, R=NM)

test_nm_haversine_3 = """
>>> round(nm_haversine_3(36.12, -86.67, 33.94, -118.40), 2)
1558.53
"""


# Subsection: How to do it...
# Topic: Creating a partial function with positional parameters

def p_haversine(
    R: float,
    lat_1: float, lon_1: float, lat_2: float, lon_2: float
) -> float:
    # etc.
    Δ_lat = radians(lat_2) - radians(lat_1)
    Δ_lon = radians(lon_2) - radians(lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    a = sqrt(
        sin(Δ_lat / 2) ** 2 +
        cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2

    )
    return R * 2 * asin(a)

from functools import partial
nm_haversine_4 = partial(p_haversine, NM)

test_nm_haversine_4 = """
>>> round(nm_haversine_4(36.12, -86.67, 33.94, -118.40), 2)
1558.53
"""


# Subsection: There's more...

nm_haversine_L = lambda *args: haversine_k(*args, R=NM)

from typing import TypeAlias
from collections.abc import Callable
NM_Hav: TypeAlias = Callable[[float, float, float, float], float]

nm_haversine_5: NM_Hav = (
	lambda lat_1, lon_1, lat_2, lon_2:
		haversine(lat_1, lon_1, lat_2, lon_2, R=NM)
)



# End of Picking an order for parameters based on partial functions

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
