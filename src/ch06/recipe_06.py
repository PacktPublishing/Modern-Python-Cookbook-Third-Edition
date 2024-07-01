# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using the OS environment settings


# Subsection: Getting ready

bash_example_1_1 = """
% python ch06/distance_app.py -u KM 36.12,-86.67 33.94,-118.40
From 36.12,-86.67 to 33.94,-118.4 in KM = 2886.90
"""

bash_example_1_2 = """
% UNITS=NM
% HOME_PORT=36.842952,-76.300171
% python ch06/distance_app.py 36.12,-86.67

From 36.12,-86.67 to 36.842952,-76.300171 in NM = 502.23
"""

# Subsection: How to do it...

import os
import sys
import argparse
from ch03.recipe_11 import haversine, MI, NM, KM
from ch06.recipe_04 import point_type, display

def get_options(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    default_units = os.environ.get("UNITS", "KM")
    if default_units not in ("KM", "NM", "MI"):
        sys.exit(f"Invalid UNITS, {default_units!r} not KM, NM, or MI")
    default_home_port = os.environ.get("HOME_PORT")
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--units",
        action="store", choices=("NM", "MI", "KM"),
        default=default_units
    )
    parser.add_argument("p1", action="store", type=point_type)
    parser.add_argument(
        "p2", nargs="?", action="store", type=point_type,
        default=default_home_port
    )
    options = parser.parse_args(argv)
    if options.p2 is None:
        sys.exit("Neither HOME_PORT nor p2 argument provided.")
    return options

# Subsection: There's more...

['ch06/distance_app.py', '-u', 'NM', '36.12,-86.67']


# End of Using the OS environment settings

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
