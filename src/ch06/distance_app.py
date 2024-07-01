# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using argparse to get command-line input

import argparse
import os
import sys
from ch06.distance_computation import haversine, MI, NM, KM


def display(
        lat1: float, lon1: float, lat2: float, lon2: float, r: str
) -> None:
    r_float = {"NM": NM, "KM": KM, "MI": MI}[r]
    d = haversine(lat1, lon1, lat2, lon2, R=r_float)
    print(f"From {lat1},{lon1} to {lat2},{lon2} in {r} = {d:.2f}")


def get_options_1(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--units", action="store", choices=("NM", "MI", "KM"), default="NM"
    )
    parser.add_argument("p1", action="store", type=point_type)
    parser.add_argument("p2", action="store", type=point_type)
    options = parser.parse_args(argv)
    return options


def get_options_2(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    default_units = os.environ.get("UNITS", "KM")
    if default_units not in ("KM", "NM", "MI"):
        sys.exit(f"Invalid UNITS, {default_units!r} not KM, NM, or MI")
    default_home_port = os.environ.get("HOME_PORT")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--units",
        action="store",
        choices=("NM", "MI", "KM"),
        default=default_units,
    )
    parser.add_argument("p1", action="store", type=point_type)
    parser.add_argument(
        "p2", nargs="?", action="store", type=point_type, default=default_home_port
    )
    options = parser.parse_args(argv)
    if options.p2 is None:
        sys.exit("Neither HOME_PORT nor p2 argument provided.")
    return options


def point_type(text: str) -> tuple[float, float]:
    try:
        lat_str, lon_str = text.split(",")
        lat = float(lat_str)
        lon = float(lon_str)
        return lat, lon
    except ValueError as ex:
        raise argparse.ArgumentTypeError(ex)


# Injecting either Recipe 4 get_options or Recipe 6 get_options
# This makes the code example suitable for both recipes.
# An alternative design is two separate apps.

from collections.abc import Callable
from typing import TypeAlias

OptionFunc: TypeAlias = Callable[[list[str]], argparse.Namespace]
injections: dict[str, OptionFunc] = {
    "4": get_options_1,
    "6": get_options_2,
}
get_options: OptionFunc = injections[os.environ.get("RECIPE", "4")]


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    lat_1, lon_1 = options.p1
    lat_2, lon_2 = options.p2
    display(lat_1, lon_1, lat_2, lon_2, r=options.units)


if __name__ == "__main__":
    main()

# ---- Tests -----

import subprocess
import os
import shlex


def bash_run(text: str) -> None:
    """
    Decompose a block of shell-like test to extract env updates, a command, and expected output.
    Set the environment, run the command, check the output.
    :raises AssertionError: if the text is unparseable or the output doesn't match.
    """
    cmd: list[str] | None = None
    local_env: dict[str, str] = {}  # {"PYTHONPATH": "."}?
    output: list[str] = []

    for line in text.strip().splitlines():
        if line.startswith("%"):
            clean = shlex.split(line.lstrip("%"))
            if "=" in clean[0]:
                var_name, value = clean[0].split("=")
                local_env[var_name.strip()] = value.strip()
            else:
                cmd = clean
        elif cmd:
            output.append(line)
        else:
            # Extra lines before the command.
            pass
    assert cmd is not None, f"no % command in {text!r}"
    assert output, f"no expected output in {text!r}"

    result = subprocess.run(
        cmd,
        env=os.environ | local_env,
        cwd="src",
        text=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )

    assert (
        result.stdout.splitlines() == output
    ), f"{result.stdout.splitlines()!r} != {output!r}"


bash_example_4_1_1 = """
% RECIPE=4  # simpler arg definition

% python ch06/distance_app.py -u KM 36.12,-86.67 33.94,-118.40
From 36.12,-86.67 to 33.94,-118.4 in KM = 2886.90
"""

bash_example_4_1_2 = """
% RECIPE=4  # simpler arg definition

% python ch06/distance_app.py -u KM 36.12,-86.67 33.94,-118asd
usage: distance_app.py [-h] [-u {NM,MI,KM}] p1 p2
distance_app.py: error: argument p2: could not convert string to float: '-118asd'
"""

bash_example_6_1_2 = """
% RECIPE=6  # more advanced arg definition

% UNITS=NM
% HOME_PORT=36.842952,-76.300171
% python ch06/distance_app.py 36.12,-86.67
From 36.12,-86.67 to 36.842952,-76.300171 in NM = 502.23
"""


def test_bash_4_1_1() -> None:
    bash_run(bash_example_4_1_1)


def test_bash_4_1_2() -> None:
    bash_run(bash_example_4_1_2)


def test_bash_6_1_2() -> None:
    bash_run(bash_example_6_1_2)
