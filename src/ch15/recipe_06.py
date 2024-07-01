# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Unit testing with the pytest module


# Subsection: Getting ready

gherkin_example = """
Scenario: Summary object can add values and compute statistics.

Given a Summary object
And numbers in the range 0 to 1000 (inclusive) shuffled randomly
When all numbers are added to the Summary object
Then the mean is 500
And the median is 500
"""


from collections import Counter
from statistics import median

test_example_class = """
class Summary:
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    def add(self, value: int) -> None: ...
    @property
    def mean(self) -> float: ...
    @property
    def median(self) -> float: ...
    @property
    def count(self) -> int: ...
    @property
    def mode(self) -> list[tuple[int, int]]: ...
"""


# Subsection: How to do it...

import random
import pytest
from recipe_01 import Summary


@pytest.fixture()
def flat_data() -> list[int]:
    data = list(range(1001))
    random.shuffle(data)
    return data


def test_flat(flat_data: list[int]) -> None:
    summary = Summary()
    for sample in flat_data:
        summary.add(sample)
    assert summary.mean == 500
    assert summary.median == 500


# Subsection: How it works...

output_example_2 = """
(cookbook3) slott@MacBookProSLott ch15 % python -m pytest recipe_06.py
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0
rootdir: /Users/slott/Documents/Writing/Python/Python Cookbook 3e
configfile: pytest.ini
plugins: anyio-4.0.0
collected 3 items                                                          

recipe_06.py ...                                                     [100%]

============================ 3 passed in 0.02s =============================
"""

output_example_3 = """
(cookbook3) slott@MacBookProSLott ch15 % python -m pytest recipe_06.py
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0
rootdir: /Users/slott/Documents/Writing/Python/Python Cookbook 3e
configfile: pytest.ini
plugins: anyio-4.0.0
collected 3 items                                                          

recipe_06.py F..                                                     [100%]

================================= FAILURES =================================
________________________________ test_flat _________________________________

flat_data = [883, 104, 898, 113, 519, 94, ...]

    def test_flat(flat_data: list[int]) -> None:
        summary = Summary()
        for sample in flat_data:
            summary.add(sample)
>       assert summary.mean == 501
E       assert 500.0 == 501
E        +  where 500.0 = <recipe_01.Summary object at 0x10fdcb350>.mean

recipe_06.py:57: AssertionError
========================= short test summary info ==========================
FAILED recipe_06.py::test_flat - assert 500.0 == 501
======================= 1 failed, 2 passed in 0.17s ========================
"""


# Subsection: There's more...


@pytest.fixture()
def summary_object(flat_data: list[int]) -> Summary:
    summary = Summary()
    for sample in flat_data:
        summary.add(sample)
    return summary

def test_mean(summary_object: Summary) -> None:
    assert summary_object.mean == 500

def test_median(summary_object: Summary) -> None:
    assert summary_object.median == 500


# End of Unit testing with the pytest module

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
