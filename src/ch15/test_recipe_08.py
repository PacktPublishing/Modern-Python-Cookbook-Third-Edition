# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Testing things that involve dates or times


gherkin_example = """
Scenario: save_date function writes JSON data to a date-stamped file.

Given a base directory Path
And a payload object {"primes": [2, 3, 5, 7, 11, 13, 17, 19]}
And a known date and time of 2017-9-10 11:12:13 UTC
When save_data(base, payload) function is executed
Then the output file of "extract_20170910111213.json" is found in the base directory
And the output file has a properly serialized version of the payload
And the datetime.datetime.now() function was called once to get the date and time
"""


# Subsection: How to do it...

import datetime
import json
from pathlib import Path

from unittest.mock import Mock
import pytest

import recipe_08


@pytest.fixture()
def mock_datetime() -> Mock:
    return Mock(
        name="mock datetime",
        datetime=Mock(
            name="mock datetime.datetime",
            now=Mock(return_value=datetime.datetime(2017, 9, 10, 11, 12, 13)),
        ),
        timezone=Mock(name="mock datetime.timezone", utc=Mock(name="UTC")),
    )


def test_save_data(
    mock_datetime: Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(recipe_08, "datetime", mock_datetime)
    data = {"primes": [2, 3, 5, 7, 11, 13, 17, 19]}
    recipe_08.save_data(tmp_path, data)
    expected_path = tmp_path / "extract_20170910111213.json"
    with expected_path.open() as result_file:
        result_data = json.load(result_file)
    assert data == result_data
    mock_datetime.datetime.now.assert_called_once_with(tz=mock_datetime.timezone.utc)


# Subsection: There's more...


@pytest.fixture()
def mock_datetime_now() -> Mock:
    return Mock(
        name="mock datetime",
        datetime=Mock(
            name="mock datetime.datetime",
            utcnow=Mock(side_effect=AssertionError("Convert to now()")),
            today=Mock(side_effect=AssertionError("Convert to now()")),
            now=Mock(return_value=datetime.datetime(2017, 7, 4, 4, 2, 3)),
        ),
    )


# End of Testing things that involve dates or times

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
