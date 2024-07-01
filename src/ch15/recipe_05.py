# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Combining unittest and doctest tests


# Subsection: Getting ready

test_example_class = '''
class Summary:
    """
    Computes summary statistics.

    >>> s = Summary()
    >>> s.add(8)
    >>> s.add(9)
    >>> s.add(9)
    >>> round(s.mean, 2)
    8.67
    >>> s.median
    9
    >>> print(str(s))
    mean = 8.67
    median = 9
    
    """
'''

import unittest
from recipe_01 import Summary

class GIVEN_Summary_WHEN_1k_samples_THEN_mean_median(unittest.TestCase):
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



# Subsection: How to do it...

import unittest
import doctest
import random
import recipe_01

def load_tests(
    loader: unittest.TestLoader, standard_tests: unittest.TestSuite, pattern: str
) -> unittest.TestSuite:
    dt = doctest.DocTestSuite(recipe_01)
    standard_tests.addTests(dt)
    return standard_tests



output_example = """
(cookbook3) % python -m unittest -v recipe_05.py
test_mean (recipe_05.GIVEN_Summary_WHEN_1k_samples_THEN_mean_median.test_mean) ... ok
test_median (recipe_05.GIVEN_Summary_WHEN_1k_samples_THEN_mean_median.test_median) ... ok
Summary (recipe_01)
Doctest: recipe_01.Summary ... ok
Twc (recipe_01)
Doctest: recipe_01.Twc ... ok
GIVEN_binom_WHEN_0_0_THEN_1 (recipe_01.__test__)
Doctest: recipe_01.__test__.GIVEN_binom_WHEN_0_0_THEN_1 ... ok
GIVEN_binom_WHEN_52_52_THEN_1 (recipe_01.__test__)
Doctest: recipe_01.__test__.GIVEN_binom_WHEN_52_52_THEN_1 ... ok
binom (recipe_01)
Doctest: recipe_01.binom ... ok
binom2 (recipe_01)
Doctest: recipe_01.binom2 ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.006s

OK

"""


# End of Combining unittest and doctest tests

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
