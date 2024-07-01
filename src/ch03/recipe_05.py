# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Forcing keyword-only arguments with the * separator


# Subsection: Getting ready

def T_wc(T: float, V: float) -> float:
    return 13.12 + 0.6215*T - 11.37*V**0.16 + 0.3965*T*V**0.16

import csv
from typing import TextIO

def wind_chill(
    start_T: int, stop_T: int, step_T: int,
    start_V: int, stop_V: int, step_V: int,
    target: TextIO
) -> None:
    """Wind Chill Table."""
    writer= csv.writer(target)
    heading = ['']+[str(t) for t in range(start_T, stop_T, step_T)]
    writer.writerow(heading)
    for V in range(start_V, stop_V, step_V):
        row = [float(V)] + [
            T_wc(T, V)
            for T in range(start_T, stop_T, step_T)
        ]
        writer.writerow(row)

test_snippet1 = """
['']+[str(t) for t in range(start_T, stop_T, step_T)]
"""

snippet2 = """
[float(V)] + [
    T_wc(T, V)
    for T in range(start_T, stop_T, step_T)
]
"""

test_example_1 = """
>>> from pathlib import Path
>>> p = Path('data/wc1.csv')
>>> with p.open('w',newline='') as target:
...     wind_chill(0, -45, -5, 0, 20, 2, target)
"""

# Subsection: How to do it...

from pathlib import Path
def wind_chill_k(
    *,
    start_T: int, stop_T: int, step_T: int,
    start_V: int, stop_V: int, step_V: int,
    target: Path
) -> None:
    ...

test_example_2 = """
>>> from io import StringIO
>>> target = StringIO()

>>> wind_chill_k(0, -45, -5, 0, 20, 2, target)
Traceback (most recent call last):
...
TypeError: wind_chill_k() takes 0 positional arguments but 7 were given
"""

test_example_3 = """
>>> p = Path('data/wc2.csv')
>>> with p.open('w', newline='') as output_file:
...     wind_chill_k(start_T=0, stop_T=-45, step_T=-5,
...     start_V=0, stop_V=20, step_V=2,
...     target=output_file)
"""

# Subsection: There's more...

import sys
from typing import TextIO

def wind_chill_k2(
    *,
    start_T: int, stop_T: int, step_T: int,
    start_V: int, stop_V: int, step_V: int,
    target: TextIO = sys.stdout
) -> None:
    ...

test_example_4 = """
>>> wind_chill_k2(
...     start_T=0, stop_T=-45, step_T=-5,
...     start_V=0, stop_V=20, step_V=2)

>>> import pathlib
>>> path = pathlib.Path("data/wc3.csv")
>>> with path.open('w', newline='') as output_file:
...     wind_chill_k2(target=output_file,
...     start_T=0, stop_T=-45, step_T=-5,
...     start_V=0, stop_V=20, step_V=2)
"""


# End of Forcing keyword-only arguments with the * separator

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
