# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Reading JSON and YAML documents


# Subection: Getting ready

{
  "teams": [
    {
      "name": "Abu Dhabi Ocean Racing",
      "position": [
        1,
        3,
        2,
        2,
        1,
        2,
        5,
        3,
        5
      ]
    },
...
  ],
  "legs": [
    "ALICANTE - CAPE TOWN",
    "CAPE TOWN - ABU DHABI",
    "ABU DHABI - SANYA",
    "SANYA - AUCKLAND",
    "AUCKLAND - ITAJA\u00cd",
    "ITAJA\u00cd - NEWPORT",
    "NEWPORT - LISBON",
    "LISBON - LORIENT",
    "LORIENT - GOTHENBURG"
  ]
}

# Subection: How to do it...

import json
from pathlib import Path

def race_summary(source_path: Path) -> None:
    document = json.loads(source_path.read_text())
    for n, leg in enumerate(document['legs']):
        print(leg)
        for team_finishes in document['teams']:
            print(
                team_finishes['name'],
                team_finishes['position'][n])

test_example_2_5 = """
>>> source_path = Path("data") / "race_result.json"
>>> document = json.loads(source_path.read_text())

>>> document['teams'][6]['name']
'Team Vestas Wind'

>>> document['legs'][5]
'ITAJAÍ - NEWPORT'
"""

# Subection: There's more...
# Topic: Serializing a complex data structure


test_example_3_1 = """
>>> import json
>>> import datetime
>>> example_date = datetime.datetime(2014, 6, 7, 8, 9, 10)
>>> document = {'date': example_date}

>>> json.dumps(document)
Traceback (most recent call last):
...
TypeError: Object of type datetime is not JSON serializable
"""

test_example_3_3 = """
>>> example_date = datetime.datetime(2014, 6, 7, 8, 9, 10)
>>> document_converted = {'date': example_date.isoformat()}

>>> json.dumps(document_converted)
'{"date": "2014-06-07T08:09:10"}'
"""

from typing import Any
import datetime

def default_date(object: Any) -> Any:
    match object:
        case datetime.datetime():
            return {"$date$": object.isoformat()}
    return object

test_example_3_5 = """
>>> example_date = datetime.datetime(2014, 6, 7, 8, 9, 10)

>>> document = {'date': example_date}
>>> print(
...     json.dumps(document, default=default_date, indent=2)
... )
{
  "date": {
    "$date$": "2014-06-07T08:09:10"
  }
}
"""

# Subection: There's more...
# Topic: Deserializing a complex data structure

from typing import Any
import datetime

def as_date(object: dict[str, Any]) -> Any:
    if {'$date$'} == set(object.keys()):
        return datetime.datetime.fromisoformat(object['$date$'])
    return object

test_example_4_2 = """
>>> source = '''{"date": {"$date$": "2014-06-07T08:09:10"}}'''

>>> json.loads(source, object_hook=as_date)
{'date': datetime.datetime(2014, 6, 7, 8, 9, 10)}
"""


# End of Reading JSON and YAML documents

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
