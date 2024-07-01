# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Unit testing with the unittest module


# Subsection: Getting ready

gherkin_example = """
Scenario: Summary object can add values and compute statistics.

Given a Summary object
And numbers in the range 0 to 1000 (inclusive) shuffled randomly
When all numbers are added to the Summary object
Then the mean is 500
And the median is 500
"""


import collections
from statistics import median
from typing import Counter

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

import unittest
import random

from recipe_01 import Summary


class GIVEN_Summary_WHEN_1k_samples_THEN_mean_median(unittest.TestCase):
    def setUp(self) -> None:
        self.summary = Summary()
        self.data = list(range(1001))
        random.shuffle(self.data)

    def runTest(self) -> None:
        for sample in self.data:
            self.summary.add(sample)
        self.assertEqual(500, self.summary.mean)
        self.assertEqual(500, self.summary.median)


if __name__ == "__main__":
    unittest.main()

bash_example = """
% python -m unittest recipe_04.py
"""

# Subsection: How it works...

output_example_1 = """
(cookbook3) % python -m unittest recipe_04.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.003s

OK

"""

output_example_2 = """
(cookbook3) % python -m unittest -v recipe_04.py
runTest (recipe_04.GIVEN_Summary_WHEN_1k_samples_THEN_mean_median.runTest) ... ok
test_mean (recipe_04.GIVEN_Summary_WHEN_1k_samples_THEN_mean_median_2.test_mean) ... FAIL
test_median (recipe_04.GIVEN_Summary_WHEN_1k_samples_THEN_mean_median_2.test_median) ... ok
test_mode (recipe_04.GIVEN_Summary_WHEN_1k_samples_THEN_mode.test_mode) ... ok

======================================================================
FAIL: test_mean (recipe_04.GIVEN_Summary_WHEN_1k_samples_THEN_mean_median_2.test_mean)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/slott/Documents/Writing/Python/Python Cookbook 3e/src/ch15/recipe_04.py", line 122, in test_mean
    self.assertEqual(501, self.summary.mean)
AssertionError: 501 != 500.0

----------------------------------------------------------------------
Ran 4 tests in 0.004s

FAILED (failures=1)

"""


# Subsection: There's more...


class GIVEN_Summary_WHEN_1k_samples_THEN_mean_median_2(unittest.TestCase):
    def setUp(self) -> None:
        self.summary = Summary()
        self.data = list(range(1001))
        random.shuffle(self.data)

        for sample in self.data:
            self.summary.add(sample)

    def test_mean(self) -> None:
        self.assertEqual(500, self.summary.mean)

    def test_median(self) -> None:
        self.assertEqual(500, self.summary.median)


# Subsection: There's more...
# Topic: Some other assertions


class GIVEN_Summary_WHEN_1k_samples_THEN_mode(unittest.TestCase):
    def setUp(self) -> None:
        self.summary = Summary()
        self.data = [500] * 97
        # Build 903 elements: each value of i occurs i times.
        for i in range(1, 43):
            self.data += [i] * i

        random.shuffle(self.data)
        for sample in self.data:
            self.summary.add(sample)

    def test_mode(self) -> None:
        top_3 = self.summary.mode[:3]
        self.assertListEqual([(500, 97), (42, 42), (41, 41)], top_3)


# Subsection: There's more...
# Topic: A separate tests directory

output_example_3 = """
(cookbook3) % (cd src; python -m unittest discover -s ch15) 
...............
----------------------------------------------------------------------
Ran 15 tests in 0.008s

OK
"""

# End of Unit testing with the unittest module

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
