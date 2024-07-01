# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Testing functions that raise exceptions


# Subsection: Getting ready

from math import factorial

def binom(n: int, k: int) -> int:
    """
    Computes the binomial coefficient.
    This shows how many combinations of
    *n* things taken in groups of size *k*.

    :param n: size of the universe
    :param k: size of each subset
    :returns: the number of combinations

    >>> binom(52, 5)
    2598960
    >>> binom(52, 0)
    1
    >>> binom(52, 52)
    1
    """

    return factorial(n) // (factorial(k) * factorial(n - k))



# Subsection: How to do it...



test_GIVEN_n_5_k_52_THEN_ValueError_1 = """
    GIVEN n=5, k=52 WHEN binom(n, k) THEN exception
    >>> binom(52, -5)
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/cookbook3/lib/python3.12/doctest.py", line 1357, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest recipe_02.__test__.test_GIVEN_n_5_k_52_THEN_ValueError[0]>", line 1, in <module>
        binom(52, -5)
      File "/Users/slott/Documents/Writing/Python/Python Cookbook 3e/src/ch15/recipe_02.py", line 29, in binom
        return factorial(n) // (factorial(k) * factorial(n - k))
                                ^^^^^^^^^^^^
    ValueError: factorial() not defined for negative values
"""

test_GIVEN_n_5_k_52_THEN_ValueError_2 = """
    GIVEN n=5, k=52 WHEN binom(n, k) THEN exception
    >>> binom(5, 52)
    Traceback (most recent call last):
    ...
    ValueError: factorial() not defined for negative values
"""

test_GIVEN_n_5_k_52_THEN_ValueError_3 = """
    GIVEN n=5, k=52 WHEN binom(n, k) THEN exception
    >>> binom(5, 52)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: factorial() not defined for negative values
"""


output_example = """
(cookbook3) % python -m doctest -v recipe_02.py
Trying:
    binom(52, -5)
Expecting:
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/cookbook3/lib/python3.12/doctest.py", line 1357, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest recipe_02.__test__.test_GIVEN_n_5_k_52_THEN_ValueError[0]>", line 1, in <module>
        binom(52, -5)
      File "/Users/slott/Documents/Writing/Python/Python Cookbook 3e/src/ch15/recipe_02.py", line 29, in binom
        return factorial(n) // (factorial(k) * factorial(n - k))
                                ^^^^^^^^^^^^
    ValueError: factorial() not defined for negative values
ok
Trying:
    binom(5, 52)  # doctest: +ELLIPSIS
Expecting:
    Traceback (most recent call last):
    ...
    ValueError: factorial() not defined for negative values
ok
Trying:
    binom(52, 5)
Expecting:
    2598960
ok
Trying:
    binom(52, 0)
Expecting:
    1
ok
Trying:
    binom(52, 52)
Expecting:
    1
ok
1 items had no tests:
    recipe_02
2 items passed all tests:
   2 tests in recipe_02.__test__.test_GIVEN_n_5_k_52_THEN_ValueError
   3 tests in recipe_02.binom
5 tests in 3 items.
5 passed and 0 failed.
Test passed.

"""

# End of Testing functions that raise exceptions

__test__ = {
    name: code
    for name, code in locals().items()
    if name.startswith("test_")
}
