# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 1: Lists and Sets
# Recipe: Deleting from a list -- deleting, removing, popping, and filtering


# Subsection: Getting ready

import csv
from pathlib import Path

def get_fuel_use(path: Path) -> list[list[str]]:
    with path.open() as source_file:
        reader = csv.reader(source_file)
        log_rows = list(reader)
    return log_rows

# Subsection: How to do it...
# Topic: The del statement

test_example_2_1 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")

>>> del log_rows[:4]
>>> log_rows[0]
['10/25/13', '08:24:00 AM', '29']

>>> log_rows[-1]
['', "choppy -- anchor in jackson's creek", '']
"""

# Subsection: How to do it...
# Topic: The remove() method

test_example_3_1 = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']
"""

test_example_3_2 = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']

>>> row.remove('')
>>> row
['10/25/13', '08:24:00 AM', '29', '01:15:00 PM', '27']
"""

snippet_3_3 = """
a = ['some', 'data']
a = a.remove('data')
"""

# Subsection: How to do it...
# Topic: The pop() method

test_example_4_1 = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']
"""

test_example_4_2 = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']

>>> target_position = row.index('')
>>> target_position
3

>>> row.pop(target_position)
''
>>> row
['10/25/13', '08:24:00 AM', '29', '01:15:00 PM', '27']
"""

# Subsection: How to do it...
# Topic: Rejecting items with the filter() function

def number_column(row: list[str], column: int = 2) -> bool:
    try:
        float(row[column])
        return True
    except ValueError:
        return False

test_example_5_2 = """
>>> log_rows = get_fuel_use(Path("data") / "fuel.csv")

>>> tail_rows = list(filter(number_column, log_rows))
>>> len(tail_rows)
4
>>> tail_rows[0]
['10/25/13', '08:24:00 AM', '29']
>>> tail_rows[-1]
['', '06:25:00 PM', '22']
"""

# Subsection: How to do it...
# Topic: Slice assignment

test_example_6_1 = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']

>>> target_position = row.index('')
>>> target_position
3
"""

test_example_6_2 = """
>>> row = ['10/25/13', '08:24:00 AM', '29', '', '01:15:00 PM', '27']

>>> row[3:4] = []
>>> row
['10/25/13', '08:24:00 AM', '29', '01:15:00 PM', '27']
"""

# Subsection: How it works...

test_example_7_1 = """
>>> row = ['', '06:25:00 PM', '22']

>>> del row[3]
Traceback (most recent call last):
...
IndexError: list assignment index out of range
"""

# Subsection: There's more...

test_example_8_1 = """
>>> data_items = [1, 1, 2, 3, 5, 8, 10,
... 13, 21, 34, 36, 55]

>>> for f in data_items:
...     if f % 2 == 0:
...         data_items.remove(f)
>>> data_items
[1, 1, 3, 5, 10, 13, 21, 36, 55]
"""

test_example_8_2 = """
>>> data_items = [1, 1, 2, 3, 5, 8, 10,
... 13, 21, 34, 36, 55]

>>> for f in data_items[:]:
...     if f % 2 == 0:
...         data_items.remove(f)
"""

test_example_8_3 = """
>>> data_items = [1, 1, 2, 3, 5, 8, 10,
... 13, 21, 34, 36, 55]

>>> position = 0
>>> while position != len(data_items):
...     f = data_items[position]
...     if f % 2 == 0:
...         data_items.remove(f)
...     else:
...         position += 1
"""


# End of Deleting from a list -- deleting, removing, popping, and filtering

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
