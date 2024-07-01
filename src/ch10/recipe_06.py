# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Including run-time valid value checks


import csv
from collections.abc import Iterator
from typing import TextIO

def tide_table_reader(source: TextIO) -> Iterator[dict[str, str]]:
    line_iter = iter(source)
    for line in line_iter:
        if len(line.rstrip()) == 0:
            break
    header = next(line_iter).rstrip().split('\t')
    del header[1]  # Extra tab in the header
    reader = csv.DictReader(line_iter, fieldnames=header, delimiter='\t')
    yield from reader


import datetime
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, PlainValidator

class HighLow(StrEnum):
    high = "H"
    low = "L"

def validate_date(v: str | datetime.date) -> datetime.date:
    match v:
        case datetime.date():
            return v
        case str():
            return datetime.datetime.strptime(v, "%Y/%m/%d").date()
        case _:
            raise TypeError("can't validate {v!r} of type {type(v)}")

class TideTable(BaseModel):
    date: Annotated[
        datetime.date,
        Field(validation_alias='Date '),
        PlainValidator(validate_date)]
    day: Annotated[
        str, Field(validation_alias='Day')]
    time: Annotated[
        datetime.time, Field(validation_alias='Time')]
    prediction: Annotated[
        float, Field(validation_alias='Pred')]
    high_low: Annotated[
        HighLow, Field(validation_alias='High/Low')]



test_tide_table = """
>>> from pathlib import Path
>>> data = Path("data") / "tide-table-2024.txt"
>>> with open(data) as tide_file:
...     dict_rows = list(tide_table_reader(tide_file))
>>> dict_rows[0]
{'Date ': '2024/04/01', 'Day': 'Mon', 'Time': '04:30', 'Pred': '-0.19', 'High/Low': 'L'}
>>> dict_rows[-1]
{'Date ': '2024/04/30', 'Day': 'Tue', 'Time': '19:57', 'Pred': '1.98', 'High/Low': 'H'}

>>> tides = [TideTable.model_validate(row) for row in dict_rows]
>>> tides[0]
TideTable(date=datetime.date(2024, 4, 1), day='Mon', time=datetime.time(4, 30), prediction=-0.19, high_low=<HighLow.low: 'L'>)
>>> tides[-1]
TideTable(date=datetime.date(2024, 4, 30), day='Tue', time=datetime.time(19, 57), prediction=1.98, high_low=<HighLow.high: 'H'>)
"""


from pydantic import (
    BaseModel, Field, PlainValidator, AfterValidator, ValidationError
)

def pass_high_tide(hl: HighLow) -> HighLow:
    assert hl == HighLow.high, f"rejected low tide"
    return hl

def pass_daylight(time: datetime.time) -> datetime.time:
    assert datetime.time(10, 0) <= time <= datetime.time(17, 0)
    return time

class HighTideTable(BaseModel):
    date: Annotated[
        datetime.date,
        Field(validation_alias='Date '),
        PlainValidator(validate_date)]
    time: Annotated[
        datetime.time,
        Field(validation_alias='Time'),
        AfterValidator(pass_daylight)]  # Range check
    prediction: Annotated[
        float,
        Field(validation_alias='Pred', ge=1.5)]  # Minimum check
    high_low: Annotated[
        HighLow,
        Field(validation_alias='High/Low'),
        AfterValidator(pass_high_tide)]  # Required value check


from collections.abc import Iterable, Iterator

def high_tide_iter(dict_reader: Iterable[dict[str, str]]) -> Iterator[HighTideTable]:
    for row in dict_reader:
        try:
            htt = HighTideTable.model_validate(row)
            yield htt
        except ValidationError as ex:
            pass  # Reject these


test_high_tide_table = """
>>> from pathlib import Path
>>> data = Path("data") / "tide-table-2024.txt"
>>> with open(data) as tide_file:
...     for ht in high_tide_iter(tide_table_reader(tide_file)):
...         print(repr(ht))
HighTideTable(date=datetime.date(2024, 4, 7), time=datetime.time(15, 42), prediction=1.55, high_low=<HighLow.high: 'H'>)
...
HighTideTable(date=datetime.date(2024, 4, 10), time=datetime.time(16, 42), prediction=2.1, high_low=<HighLow.high: 'H'>)
...
HighTideTable(date=datetime.date(2024, 4, 26), time=datetime.time(16, 41), prediction=2.19, high_low=<HighLow.high: 'H'>)

"""


def validate_date_time(v: str | datetime.datetime) -> datetime.datetime:
    match v:
        case datetime.datetime():
            return v
        case str():
            return datetime.datetime.strptime(v, "%Y/%m/%d %H:%M")
    raise TypeError(f"can't validate {v} of type {type(v)}")

def pass_daylight2(timestamp: datetime.datetime) -> datetime.datetime:
    assert datetime.time(10, 0) <= timestamp.time() <= datetime.time(17, 0)
    return timestamp


from pydantic import model_validator, AfterValidator
from typing import Any

class HighTideTable2(BaseModel):
    timestamp: Annotated[
        datetime.datetime,
        Field(validation_alias='Date-Time'),
        PlainValidator(validate_date_time),
        AfterValidator(pass_daylight2)]
    prediction: Annotated[
        float,
        Field(validation_alias='Pred', ge=1.5)]
    high_low: Annotated[
        HighLow,
        Field(validation_alias='High/Low'),
        AfterValidator(pass_high_tide)]

    @model_validator(mode='before')
    @classmethod
    def combine_datestamp(cls, data: Any) -> Any:
        match data:
            case dict():
                data['Date-Time'] = f"{data['Date ']} {data['Time']}"
                return data
            case HighTideTable2():
                return data
        raise TypeError(f"can't validate {data} of type {type(data)}")

def high_tide_2_iter(dict_reader: Iterable[dict[str, str]]) -> Iterator[HighTideTable2]:
    for row in dict_reader:
        try:
            htt = HighTideTable2.model_validate(row)
            yield htt
        except ValidationError as ex:
            pass  # Skip these

test_high_tide_table_2 = """
>>> from pathlib import Path
>>> data = Path("data") / "tide-table-2024.txt"
>>> with open(data) as tide_file:
...     for ht in high_tide_2_iter(tide_table_reader(tide_file)):
...         print(repr(ht))
HighTideTable2(timestamp=datetime.datetime(2024, 4, 7, 15, 42), prediction=1.55, high_low=<HighLow.high: 'H'>)
...
HighTideTable2(timestamp=datetime.datetime(2024, 4, 10, 16, 42), prediction=2.1, high_low=<HighLow.high: 'H'>)
...
HighTideTable2(timestamp=datetime.datetime(2024, 4, 26, 16, 41), prediction=2.19, high_low=<HighLow.high: 'H'>)
"""

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
