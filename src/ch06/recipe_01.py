# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using the features of the print() function




test_example_1_1 = """
>>> print("Hello, world.")
Hello, world.
"""

test_example_1_2 = """
>>> count = 9973
>>> print("Final count", count)
Final count 9973
"""

# Subsection: Getting ready

data = """
date,engine on,fuel height on,engine off,fuel height off
10/25/13,08:24:00,29,13:15:00,27
10/26/13,09:12:00,27,18:25:00,22
10/28/13,13:21:00,22,06:25:00,14
"""

from pathlib import Path
import csv

def get_fuel_use(source_path: Path) -> list[dict[str, str]]:
    with source_path.open() as source_file:
        rdr = csv.DictReader(source_file)
        return list(rdr)

test_example_2_3 = """
>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = get_fuel_use(source_path)
>>> for row in fuel_use:
...     print(row)
{'date': '10/25/13', 'engine on': '08:24:00', 'fuel height on': '29', 'engine off': '13:15:00', 'fuel height off': '27'}
{'date': '10/26/13', 'engine on': '09:12:00', 'fuel height on': '27', 'engine off': '18:25:00', 'fuel height off': '22'}
{'date': '10/28/13', 'engine on': '13:21:00', 'fuel height on': '22', 'engine off': '06:25:00', 'fuel height off': '14'}
"""

# Subsection: How to do it...


test_example_3_1 = """
>>> fuel_use = get_fuel_use(Path("data/fuel2.csv"))

>>> for leg in fuel_use:
...     start = float(leg["fuel height on"])
...     finish = float(leg["fuel height off"])

...     print("On", leg["date"], "from", leg["engine on"],
...         "to", leg["engine off"],
...         "change", start-finish, "in.")
On 10/25/13 from 08:24:00 to 13:15:00 change 2.0 in.
On 10/26/13 from 09:12:00 to 18:25:00 change 5.0 in.
On 10/28/13 from 13:21:00 to 06:25:00 change 8.0 in.

...     print(leg["date"], leg["engine on"],
...         leg["engine off"], start-finish, sep=" | ")
10/25/13 | 08:24:00 | 13:15:00 | 2.0
10/26/13 | 09:12:00 | 18:25:00 | 5.0
10/28/13 | 13:21:00 | 06:25:00 | 8.0

...     print("date", leg["date"], sep="=", end=", ")
...     print("on", leg["engine on"], sep="=", end=", ")
...     print("off", leg["engine off"], sep="=", end=", ")
...     print("change", start-finish, sep="=")
date=10/25/13, on=08:24:00, off=13:15:00, change=2.0
date=10/26/13, on=09:12:00, off=18:25:00, change=5.0
date=10/28/13, on=13:21:00, off=06:25:00, change=8.0
"""

# Subsection: How it works...

from typing import TextIO, Any
import sys

def print_like(
        *args: Any,
        sep: str = " ",
        end: str = "\n",
        file: TextIO | None = None,
        flush: bool = False
) -> None:
    if file is None:
        file = sys.stdout
    arg_iter = iter(args)
    value = next(arg_iter)
    file.write(str(value))
    for value in arg_iter:
        file.write(sep)
        file.write(str(value))
    file.write(end)
    if flush: file.flush()

# Subsection: There's more...

test_example_5_1 = """
>>> import sys

>>> print("Red Alert!", file=sys.stderr)
"""

bash_example_5_2 = """
% python myapp.py < input.dat > output.dat
"""


test_example_5_3 = """
>>> from pathlib import Path
>>> target_path = Path("data")/"extra_detail.log"
>>> with target_path.open('w') as target_file:
...     print("Some detailed output", file=target_file)
...     print("Ordinary log")
Ordinary log
"""


# End of Using the features of the print() function

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
