# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Essential type hints for class definitions

from recipe_02 import Dice

def example_mypy_failure() -> None:
    d = Dice(2.5)
    d.first_roll()
    print(d)

def another_mypy_problem() -> None:
    d = Dice(6)
    r1: list[str] = d.first_roll()
    print(r1)

error_examples = """
% mypy src/ch07/recipe_02_bad.py
src/ch07/recipe_02_bad.py:9: error: Argument 1 to "Dice" has incompatible type "float"; expected "int"  [arg-type]
src/ch07/recipe_02_bad.py:20: error: Incompatible types in assignment (expression has type "list[int]", variable has type "list[str]")  [assignment]
Found 2 errors in 1 file (checked 1 source file)
"""

