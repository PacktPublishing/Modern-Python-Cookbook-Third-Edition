# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Mocking external resources


gherkin_example = """
Scenario: save_data() function is broken.

Given some faulty set of data, "faulty_data", that causes a failure in the save_data() function
And an existing file, "important_data.csv"
When safe_write("important_data.csv", faulty_data) is processed
Then safe_write raises an exception
And the existing file, "important_data.csv" is untouched
"""


# Subsection: How to do it...

from pathlib import Path
from typing import Any

from unittest.mock import Mock, sentinel
import pytest

import recipe_10


@pytest.fixture()
def original_file(tmp_path: Path) -> Path:
    precious_file = tmp_path / "important_data.csv"
    precious_file.write_text(hex(id(sentinel.ORIGINAL_DATA)), encoding="utf-8")
    return precious_file


def save_data_good(path: Path, content: recipe_10.Quotient) -> None:
    path.write_text(hex(id(sentinel.GOOD_DATA)), encoding="utf-8")


def test_safe_write_happy(original_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mock_save_data = Mock(side_effect=save_data_good)
    monkeypatch.setattr(recipe_10, "save_data", mock_save_data)
    data = recipe_10.Quotient(355, 113)
    recipe_10.safe_write(Path(original_file), data)
    actual = original_file.read_text(encoding="utf-8")

    assert actual == hex(id(sentinel.GOOD_DATA))


def save_data_failure(path: Path, content: recipe_10.Quotient) -> None:
    path.write_text(hex(id(sentinel.CORRUPT_DATA)), encoding="utf-8")
    raise RuntimeError("mock exception")


def test_safe_write_scenario_2(
    original_file: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mock_save_data = Mock(side_effect=save_data_failure)
    monkeypatch.setattr(recipe_10, "save_data", mock_save_data)
    data = recipe_10.Quotient(355, 113)
    with pytest.raises(RuntimeError) as ex:
        recipe_10.safe_write(Path(original_file), data)
    actual = original_file.read_text(encoding="utf-8")
    assert actual == hex(id(sentinel.ORIGINAL_DATA))


# Subsection: There's more...

from unittest.mock import Mock, sentinel, call


def test_safe_write_scenarios(
        original_file: Path,
        mock_pathlib_path: Mock,
        monkeypatch: pytest.MonkeyPatch
) -> None:
    mock_save_data = Mock(side_effect=save_data_good)
    monkeypatch.setattr(recipe_10, "save_data", mock_save_data)
    data = recipe_10.Quotient(355, 113)
    with pytest.raises(RuntimeError) as exc_info:
        recipe_10.safe_write(mock_pathlib_path, data)
    actual = original_file.read_text(encoding="utf-8")
    assert actual == hex(id(sentinel.ORIGINAL_DATA))
    mock_save_data.assert_called_once()
    mock_pathlib_path.with_suffix.mock_calls == [
        call("suffix.new"), call("suffix.old")
    ]
    # Scenario-specific details...
    if exc_info.value.args == ("3",):
        pass
    elif exc_info.value.args == ("4",):
        mock_pathlib_path.rename.assert_called_once()
    elif exc_info.value.args == ("5",):
        mock_pathlib_path.rename.assert_called_once()
    else:
        assert False, f"unexpected value for {exc_info.value.args=}"


scenario_3 = {
    "original": None, "new": None, "old": RuntimeError("3")}

scenario_4 = {
    "original": RuntimeError("4"), "new": None, "old": None}

scenario_5 = {
    "original": None, "new": RuntimeError("5"), "old": None}


@pytest.fixture(
    params=[scenario_3, scenario_4, scenario_5],
)
def mock_pathlib_path(request: pytest.FixtureRequest) -> Mock:
    mock_mapping = request.param
    new_path = Mock(rename=Mock(side_effect=mock_mapping["new"]))
    old_path = Mock(unlink=Mock(side_effect=mock_mapping["old"]))
    output_path = Mock(
        name="mock output_path",
        suffix="suffix",
        with_suffix=Mock(side_effect=[new_path, old_path]),
        rename=Mock(side_effect=mock_mapping["original"]),
    )
    return output_path


example_output = """
(cookbook3) % pytest -v test_recipe_10.py
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0 -- /Users/slott/miniconda3/envs/cookbook3/bin/python
cachedir: .pytest_cache
rootdir: /Users/slott/Documents/Writing/Python/Python Cookbook 3e
configfile: pytest.ini
plugins: anyio-4.0.0
collected 5 items

test_recipe_10.py::test_safe_write_happy PASSED                      [ 20%]
test_recipe_10.py::test_safe_write_scenario_2 PASSED                 [ 40%]
test_recipe_10.py::test_safe_write_scenarios[scenario_3] PASSED      [ 60%]
test_recipe_10.py::test_safe_write_scenarios[scenario_4] PASSED      [ 80%]
test_recipe_10.py::test_safe_write_scenarios[scenario_5] PASSED      [100%]

============================ 5 passed in 0.07s =============================
"""

# End of Mocking external resources

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
