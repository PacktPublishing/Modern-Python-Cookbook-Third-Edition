# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Controlling the order of dictionary keys


# Subsection: Getting ready

data = """
date,engine on,fuel height on,engine off,fuel height off
10/25/13,08:24:00,29,13:15:00,27
10/26/13,09:12:00,27,18:25:00,22
10/28/13,13:21:00,22,06:25:00,14
"""

# Subsection: How to do it...

import csv
from pathlib import Path

def get_fuel_use(source_path: Path) -> list[dict[str, str]]:
    with source_path.open() as source_file:
        rdr = csv.DictReader(source_file)
        data: list[dict[str, str]] = list(rdr)
    return data

test_example_2_2 = """
>>> from pprint import pprint

>>> source_path = Path("data/fuel2.csv")
>>> fuel_use = get_fuel_use(source_path)
>>> for row in fuel_use:
...     pprint(row)
{'date': '10/25/13',
 'engine off': '13:15:00',
 'engine on': '08:24:00',
 'fuel height off': '27',
 'fuel height on': '29'}
{'date': '10/26/13',
 'engine off': '18:25:00',
 'engine on': '09:12:00',
 'fuel height off': '22',
 'fuel height on': '27'}
{'date': '10/28/13',
 'engine off': '06:25:00',
 'engine on': '13:21:00',
 'fuel height off': '14',
 'fuel height on': '22'}
"""

# Subsection: How it works...

test_example_3_1 = """
>>> row = {'columns': 42, 'data': 3.14, 'of': 2.718, 'some': 1.618}

>>> key_order = ['some', 'columns', 'of', 'data']
>>> dict(
...     [(name, row[name]) for name in key_order]
... )
{'some': 1.618, 'columns': 42, 'of': 2.718, 'data': 3.14}
"""

# Subsection: There's more...

snippet_4_1 = """
for field in row:
    print(field, row[field])
"""


test_example_4_2 = """
>>> log_rows = [
... {'date': '2019-11-12T13:14:15', 'path': '/path/to/resource'},
... {'date': '2019-11-14T15:16:17', 'path': '/path/to/resource'},
... {'date': '2019-11-19T20:21:11', 'path': '/path/to/resource'},
... {'date': '2019-11-20T21:22:23', 'path': '/path/to/resource'},
... {'date': '2019-11-26T07:08:09', 'path': '/path/to/resource'},
... ]

>>> import collections
>>> import datetime
>>> summary = collections.Counter()
>>> for row in log_rows:
...     date = datetime.datetime.strptime(row['date'], "%Y-%m-%dT%H:%M:%S")
...     summary[date.weekday()] += 1

>>> summary
Counter({1: 3, 3: 1, 2: 1})


>>> import calendar
>>> for k in sorted(summary):
...     print(calendar.day_name[k], summary[k])
Tuesday 3
Wednesday 1
Thursday 1
"""


# End of Controlling the order of dictionary keys

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
