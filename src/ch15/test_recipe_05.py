# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Combining unittest and doctest tests

# Subsection: There's more...

import doctest
import unittest

import recipe_01 as ch15_r01
import recipe_02 as ch15_r02
import recipe_03 as ch15_r03
import recipe_05 as ch15_r04

def load_tests(
    loader: unittest.TestLoader, standard_tests: unittest.TestSuite, pattern: str
) -> unittest.TestSuite:
    for module in (ch15_r01, ch15_r02, ch15_r03, ch15_r04):
        dt = doctest.DocTestSuite(module)
        standard_tests.addTests(dt)
    return standard_tests


output_example = """
(cookbook3) slott@MacBookProSLott Python Cookbook 3e % (cd src/ch15; python -m unittest -v test_recipe_05.py)
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
test_GIVEN_n_5_k_52_THEN_ValueError (recipe_02.__test__)
Doctest: recipe_02.__test__.test_GIVEN_n_5_k_52_THEN_ValueError ... ok
binom (recipe_02)
Doctest: recipe_02.binom ... ok
test_example_2_1 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_2_1 ... ok
test_example_2_3 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_2_3 ... ok
test_example_3_1 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_3_1 ... ok
test_example_3_3 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_3_3 ... ok
test_example_3_4 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_3_4 ... ok
test_example_4_1 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_4_1 ... ok
test_example_4_2 (recipe_03.__test__)
Doctest: recipe_03.__test__.test_example_4_2 ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.013s

OK
"""
