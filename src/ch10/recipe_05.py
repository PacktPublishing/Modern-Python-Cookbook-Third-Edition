# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Implementing more strict type checks with pydantic


data = """
[2016-06-15 17:57:54,715] INFO in ch10_r10: Sample Message One
[2016-06-15 17:57:54,716] DEBUG in ch10_r10: Debugging
[2016-06-15 17:57:54,720] WARNING in ch10_r10: Something might have gone wrong
"""

import re

pattern = re.compile(
    r"\[(?P<date>.*?)\]\s+"
    r"(?P<level>\w+)\s+"
    r"in\s+(?P<module>.+?)"
    r":\s+(?P<message>.+)",
    re.X
)


import datetime
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field

class LevelClass(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class LogData(BaseModel):
    date: datetime.datetime
    level: LevelClass
    module: Annotated[str, Field(pattern=r'^\w+$')]
    message: str

from typing import Iterable, Iterator

def logdata_iter(source: Iterable[str]) -> Iterator[LogData]:
    for row in source:
        if match := pattern.match(row):
            l = LogData.model_validate(match.groupdict())
            yield l

test_logdata = """
>>> from pprint import pprint
>>> pprint(list(logdata_iter(data.splitlines())))
[LogData(date=datetime.datetime(2016, 6, 15, 17, 57, 54, 715000), level=<LevelClass.INFO: 'INFO'>, module='ch10_r10', message='Sample Message One'),
 LogData(date=datetime.datetime(2016, 6, 15, 17, 57, 54, 716000), level=<LevelClass.DEBUG: 'DEBUG'>, module='ch10_r10', message='Debugging'),
 LogData(date=datetime.datetime(2016, 6, 15, 17, 57, 54, 720000), level=<LevelClass.WARNING: 'WARNING'>, module='ch10_r10', message='Something might have gone wrong')]
 
>>> for record in logdata_iter(data.splitlines()):
...     print(record.model_dump_json())
{"date":"2016-06-15T17:57:54.715000","level":"INFO","module":"ch10_r10","message":"Sample Message One"}
{"date":"2016-06-15T17:57:54.716000","level":"DEBUG","module":"ch10_r10","message":"Debugging"}
{"date":"2016-06-15T17:57:54.720000","level":"WARNING","module":"ch10_r10","message":"Something might have gone wrong"}

>>> import json
>>> print(json.dumps(LogData.model_json_schema(), indent=2))
{
  "$defs": {
    "LevelClass": {
      "enum": [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR"
      ],
      "title": "LevelClass",
      "type": "string"
    }
  },
  "properties": {
    "date": {
      "format": "date-time",
      "title": "Date",
      "type": "string"
    },
    "level": {
      "$ref": "#/$defs/LevelClass"
    },
    "module": {
      "pattern": "^\\\\w+$",
      "title": "Module",
      "type": "string"
    },
    "message": {
      "title": "Message",
      "type": "string"
    }
  },
  "required": [
    "date",
    "level",
    "module",
    "message"
  ],
  "title": "LogData",
  "type": "object"
}

"""


__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
