# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using argparse to get command-line input


bash_example_1_1 = """
% python ch06/distance_app.py -u KM 36.12,-86.67 33.94,-118.40
From 36.12,-86.67 to 33.94,-118.4 in KM = 2886.90
"""

bash_example_1_2 = """
% python ch06/distance_app.py -u KM 36.12,-86.67 33.94,-118asd
usage: distance_app.py [-h] [-u {NM,MI,KM}] p1 p2
distance_app.py: error: argument p2: could not convert string to float: '-118asd'
"""

# Subsection: Getting ready

from ch03.recipe_11 import haversine, MI, NM, KM

def display(lat1: float, lon1: float, lat2: float, lon2: float, r: str) -> None:
    r_float = {"NM": NM, "KM": KM, "MI": MI}[r]
    d = haversine(lat1, lon1, lat2, lon2, R=r_float)
    print(f"From {lat1},{lon1} to {lat2},{lon2} in {r} = {d:.2f}")

test_example_2_2 = """
>>> display(36.12, -86.67, 33.94, -118.4, 'NM')
From 36.12,-86.67 to 33.94,-118.4 in NM = 1558.53
"""

# Subsection: How to do it...

import argparse
import sys

def get_options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--units",
        action="store", choices=("NM", "MI", "KM"), default="NM")
    parser.add_argument("p1", action="store", type=point_type)
    parser.add_argument("p2", action="store", type=point_type)
    options = parser.parse_args(argv)
    return options

def point_type(text: str) -> tuple[float, float]:
    try:
        lat_str, lon_str = text.split(",")
        lat = float(lat_str)
        lon = float(lon_str)
        return lat, lon
    except ValueError as ex:
        raise argparse.ArgumentTypeError(ex)

def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    lat_1, lon_1 = options.p1
    lat_2, lon_2 = options.p2
    display(lat_1, lon_1, lat_2, lon_2, r=options.r)

if __name__ == "__main__":
    main()

# Subsection: How it works...

base_example_4_1 = """
% python some_program.py *.rst
"""

from pathlib import Path

def get_options_2(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=Path, nargs='*')
    options = parser.parse_args(argv)
    return options

def process(path: Path) -> None:
    pass

def some_app(options: argparse.Namespace) -> None:
    for filename in options.file:
        process(filename)


import platform
from pathlib import Path

def get_options_windows(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=Path, nargs='*')
    options = parser.parse_args(argv)

    if platform.system() == "Windows":
        options.file = list(
            name
            for wildcard in options.file
            for name in Path().glob(wildcard)
        )
    return options

# End of Using argparse to get command-line input

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
