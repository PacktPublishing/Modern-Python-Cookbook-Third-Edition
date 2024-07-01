# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Testing things that involve randomness


gherkin_example = """
Given a random number generator where choice() always return the sequence [23, 29, 31, 37, 41, 43, 47, 53]
When we evaluate the expression resample(any 8 values, 8)
Then the expected results are [23, 29, 31, 37, 41, 43, 47, 53]
And the choice() function was called 8 times
"""


# Subsection: How to do it...

from unittest.mock import Mock
import pytest
import recipe_09


@pytest.fixture()
def expected_resample_data() -> list[int]:
    return [23, 29, 31, 37, 41, 43, 47, 53]

@pytest.fixture()
def mock_random_choice(expected_resample_data: list[int]) -> Mock:
    mock_choice = Mock(name="mock random.choice", side_effect=expected_resample_data)
    return mock_choice



def test_resample(
    mock_random_choice: Mock,
    expected_resample_data: list[int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(recipe_09.random, "choice", mock_random_choice)  # type: ignore [attr-defined]
    data = [2, 3, 5, 7, 11, 13, 17, 19]
    resample_data = list(recipe_09.resample(data, 8))
    assert resample_data == expected_resample_data
    assert mock_random_choice.mock_calls == 8 * [call(data)]


# Subsection: There's more...

from collections.abc import Iterator
from typing import Any


def another_function(X: Any) -> Any:
    return None


def resample_pattern(X: Any, Y: Any) -> Iterator[Any]:
    for _ in range(Y):
        yield another_function(X)


from unittest.mock import Mock, call, sentinel

@pytest.fixture()
def mock_choice_s() -> Mock:
    mock_choice = Mock(name="mock random.choice()", return_value=sentinel.CHOICE)
    return mock_choice

def test_resample_2(
        mock_choice_s: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        recipe_09.random, "choice", mock_choice_s # type: ignore [attr-defined]
    )
    resample_data = list(recipe_09.resample(sentinel.POPULATION, 8))
    assert resample_data == [sentinel.CHOICE] * 8
    assert mock_choice_s.mock_calls == 8 * [call(sentinel.POPULATION)]


# End of Testing things that involve randomness

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
