# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 1: Lists and Sets
# Recipe: Slicing and dicing a list


# Subsection: Getting ready

import csv
from pathlib import Path

def get_fuel_use(path: Path) -> list[list[str]]:
    with path.open() as source_file:
        reader = csv.reader(source_file)
        log_rows = list(reader)
    return log_rows

test_example_1_2 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")

>>> log_rows[0]
['date', 'engine on', 'fuel height']

>>> log_rows[-1]
['', "choppy -- anchor in jackson's creek", '']
"""

# Subsection: How to do it...

test_example_2_1 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")

>>> head, tail = log_rows[:4], log_rows[4:]
>>> head[0]
['date', 'engine on', 'fuel height']
>>> head[-1]
['', '', '']
>>> tail[0]
['10/25/13', '08:24:00 AM', '29']
>>> tail[-1]
['', "choppy -- anchor in jackson's creek", '']
"""

test_example_2_2 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")
>>> head, tail = log_rows[:4], log_rows[4:]

>>> from pprint import pprint
>>> pprint(tail[0::3], width=64)
[['10/25/13', '08:24:00 AM', '29'],
 ['10/26/13', '09:12:00 AM', '27']]
"""

test_example_2_3 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")
>>> head, tail = log_rows[:4], log_rows[4:]

>>> from pprint import pprint
>>> pprint(tail[1::3], width=48)
[['', '01:15:00 PM', '27'],
 ['', '06:25:00 PM', '22']]
"""

test_example_2_4 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")
>>> head, tail = log_rows[:4], log_rows[4:]

>>> from pprint import pprint
>>> paired_rows = list(zip(tail[0::3], tail[1::3]))
>>> pprint(paired_rows)
[(['10/25/13', '08:24:00 AM', '29'], ['', '01:15:00 PM', '27']),
 (['10/26/13', '09:12:00 AM', '27'], ['', '06:25:00 PM', '22'])]
"""

test_example_2_5 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")
>>> head, tail = log_rows[:4], log_rows[4:]

>>> from pprint import pprint
>>> paired_rows = list(zip(tail[0::3], tail[1::3]))
>>> combined = [a+b for a, b in paired_rows]
>>> pprint(combined)
[['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27'],
 ['10/26/13', '09:12:00 AM', '27', '', '06:25:00 PM', '22']]
"""


# End of Slicing and dicing a list

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
