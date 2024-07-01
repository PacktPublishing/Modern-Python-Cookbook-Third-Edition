# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using input() and getpass() for user  input


# Subsection: Getting ready

import pytest
import builtins

from datetime import date

def get_date1() -> date:
    year = int(input("year: "))
    month = int(input("month [1-12]: "))
    day = int(input("day [1-31]: "))
    result = date(year, month, day)
    return result


from unittest.mock import Mock
def test_get_date1(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, 'input', Mock(side_effect=["2023", "1", "18"]))
    d = get_date1()
    assert d == datetime.date(2023, 1, 18)

# Subsection: How to do it...

from getpass import getpass

def get_year_1() -> int:
    year_text = input("year: ")
    year = int(year_text)
    return year

def test_get_year_1(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, 'input', Mock(side_effect=["2023"]))
    d = get_year_1()
    assert d == 2023

def get_year() -> int:
    year = None
    while year is None:
        year_text = input("year: ")
        try:
            year = int(year_text)
        except ValueError as ex:
            print(ex)
    return year

def test_get_year(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(builtins, 'input', Mock(side_effect=["abx", "2023"]))
    d = get_year()
    assert d == 2023
    out, err = capsys.readouterr()
    assert out == "invalid literal for int() with base 10: 'abx'\n"

def get_integer(prompt: str) -> int:
    while True:
        value_text = input(prompt)
        try:
            value = int(value_text)
            return value
        except ValueError as ex:
            print(ex)

def test_get_integer(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(builtins, 'input', Mock(side_effect=["abx", "2023"]))
    d = get_integer('year: ')
    assert d == 2023
    out, err = capsys.readouterr()
    assert out == "invalid literal for int() with base 10: 'abx'\n"


def get_date2() -> date:
    while True:
        year = get_integer("year: ")
        month = get_integer("month [1-12]: ")
        day = get_integer("day [1-31]: ")
        try:
            result = date(year, month, day)
            return result
        except ValueError as ex:
            print(f"invalid, {ex}")

def test_get_date2(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, 'input', Mock(side_effect=["2023", "1", "18"]))
    d = get_date2()
    assert d == datetime.date(2023, 1, 18)

# Subsection: There's more...
# Topic: Complex text parsing

import datetime

def get_date3() -> date:
    while True:
        raw_date_str = input("date [yyyy-mm-dd]: ")
        try:
            input_date = datetime.datetime.strptime(
                raw_date_str, "%Y-%m-%d").date()
            return input_date
        except ValueError as ex:
            print(f"invalid date, {ex}")

def test_get_date3(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(builtins, 'input', Mock(side_effect=["2023-1-18"]))
    d = get_date3()
    assert d == datetime.date(2023, 1, 18)


# End of Using input() and getpass() for user  input

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
