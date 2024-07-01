# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using invoke to get command-line input

import sys
from invoke.tasks import task
from invoke.context import Context

from ch06.distance_computation import haversine, MI, NM, KM


def display(
        lat1: float, lon1: float, lat2: float, lon2: float, r: str
) -> None:
    r_float = {"NM": NM, "KM": KM, "MI": MI}[r]
    d = haversine(lat1, lon1, lat2, lon2, R=r_float)
    print(f"From {lat1},{lon1} to {lat2},{lon2} in {r} = {d:.2f}")


def point_type(text: str) -> tuple[float, float]:
    lat_str, lon_str = text.split(",")
    lat = float(lat_str)
    lon = float(lon_str)
    return lat, lon

@task(
    help={
        'p1': 'Lat,Lon',
        'p2': 'Lat,Lon',
        'u': 'Unit: KM, MI, NM'})
def distance(
        context: Context, p1: str, p2: str, u: str = "KM"
) -> None:
    """Compute distance between two points.
    """
    try:
        lat_1, lon_1 = point_type(p1)
        lat_2, lon_2 = point_type(p2)
        display(lat_1, lon_1, lat_2, lon_2, r=u)
    except (ValueError, KeyError) as ex:
        sys.exit(f"{ex}\nFor help use invoke --help distance")


# ---- Tests -----

import subprocess
import os
import shlex
from pathlib import Path


def bash_run(text: str) -> None:
    """
    Decompose a block of shell-like test to extract env updates, a command, and expected output.
    Set the environment, run the command, check the output.
    :raises AssertionError: if the text is unparseable or the output doesn't match.
    """
    cmd: list[str] | None = None
    local_env: dict[str, str] = {"PYTHONPATH": str(Path.cwd() / "src")}
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
        cwd="src/ch06",
        text=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )

    assert (
        result.stdout.splitlines() == output
    ), f"{result.stdout.splitlines()!r} != {output!r}"


bash_example_7_1_1 = """
% RECIPE=7  # invoke

% invoke distance -u KM 36.12,-86.67 33.94,-118.40
From 36.12,-86.67 to 33.94,-118.4 in KM = 2886.90
"""

bash_example_7_1_2 = """
% RECIPE=7  # invoke

% invoke distance -u KM 36.12,-86.67 33.94,-118asd
could not convert string to float: '-118asd'
For help use invoke --help distance
"""


def test_bash_7_1_1() -> None:
    bash_run(bash_example_7_1_1)


def test_bash_7_1_2() -> None:
    bash_run(bash_example_7_1_2)

