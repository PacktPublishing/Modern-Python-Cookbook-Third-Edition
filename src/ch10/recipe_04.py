# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Handling type conversions


from math import radians, sin, cos, sqrt, asin
MI = 3959
NM = 3440
KM = 6373

def haversine(
    lat_1: float, lon_1: float,
    lat_2: float, lon_2: float, *, R: float) -> float:

    ...  # etc.
    Δ_lat = radians(lat_2) - radians(lat_1)
    Δ_lon = radians(lon_2) - radians(lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    a = sqrt(
        sin(Δ_lat / 2) ** 2 +
        cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2

    )
    return R * 2 * asin(a)

from ast import literal_eval

def distance(
    *args: str | float | tuple[float, float],
    R: float = NM
) -> float:
    match args:
        case [float(lat_1), float(lon_1), float(lat_2), float(lon_2)]:
            pass
        case (
            [[float(lat_1), float(lon_1)],
             [float(lat_2), float(lon_2)]]
        ):
            pass
        case [str(s1), str(s2), str(s3), str(s4)]:
            lat_1, lon_1, lat_2, lon_2 = (
                float(s1), float(s2), float(s3), float(s4)
            )
        case [str(ll1), str(ll2)]:
            lat_1, lon_1 = literal_eval(ll1)
            lat_2, lon_2 = literal_eval(ll2)
        case (
             {"lat": float(lat_1), "lon": float(lon_1)},
             {"lat": float(lat_2), "lon": float(lon_2)}
        ):
            pass
        case _:
            raise ValueError(f"unexpected types in {args!r}")
    return haversine(lat_1, lon_1, lat_2, lon_2, R=R)


test_distance = """
>>> round(distance(36.12, -86.67, 33.94, -118.40, R=6372.8), 2)
2887.26
>>> round(distance("36.12", "-86.67", "33.94", "-118.40", R=6372.8), 2)
2887.26
>>> round(distance("36.12,-86.67", "33.94,-118.40", R=6372.8), 2)
2887.26
>>> round(distance((36.12, -86.67), (33.94, -118.40), R=6372.8), 2)
2887.26

>>> round(distance(5, 6, 7, 8, R=6372.8), 2)
Traceback (most recent call last):
...
ValueError: unexpected types in (5, 6, 7, 8)

"""

test_distance_more = """
>>> round(distance({"lat": 36.12, "lon": -86.67}, {"lat": 33.94, "lon": -118.40}, R=6372.8), 2)
2887.26

>>> round(distance("36.12,-86.67", (33.94, -118.40), R=6372.8), 2)
Traceback (most recent call last):
...
ValueError: unexpected types in ('36.12,-86.67', (33.94, -118.4))

"""

from typing import TypeAlias
Point: TypeAlias = str | tuple[float, float] | tuple[str, str] | dict[str, float]

def distance_2(
    *args: Point | float,
    R: float = NM
) -> float:
    def parse(item: Point | float) -> tuple[float, float]:
        match item:
            case [float(lat), float(lon)]:
                pass
            case {"lat": float(lat), "lon": float(lon)}:
                pass
            case str(sll):
                lat, lon = literal_eval(sll)
            case _:
                raise ValueError(f"unexpected types in {item!r}")
        return lat, lon

    match args:
        case [float(lat_1), float(lon_1), float(lat_2), float(lon_2)]:
            pass
        case [str(s1), str(s2), str(s3), str(s4)]:
            lat_1, lon_1, lat_2, lon_2 = float(s1), float(s2), float(s3), float(s4)
        case [p_1, p_2]:
            lat_1, lon_1 = parse(p_1)
            lat_2, lon_2 = parse(p_2)
        case _:
            raise ValueError(f"unexpected types in {args!r}")
    return haversine(lat_1, lon_1, lat_2, lon_2, R=R)


test_distance_more_solved = """
>>> round(distance_2({"lat": 36.12, "lon": -86.67}, {"lat": 33.94, "lon": -118.40}, R=6372.8), 2)
2887.26

>>> round(distance_2("36.12,-86.67", (33.94, -118.40), R=6372.8), 2)
2887.26


"""

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
