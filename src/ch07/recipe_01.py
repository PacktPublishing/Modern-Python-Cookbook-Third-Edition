# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Using a class to encapsulate data and processing


# Subection: How to do it...

from random import randint


class Dice:
    def __init__(self) -> None:
        self.faces: tuple[int, int] = (0, 0)
    def roll(self) -> None:
        self.faces = (randint(1,6), randint(1,6))
    def total(self) -> int:
        return sum(self.faces)
    def hardway(self) -> bool:
        return self.faces[0] == self.faces[1]
    def easyway(self) -> bool:
        return self.faces[0] != self.faces[1]

test_example_1_6 = """
>>> import random
>>> random.seed(1)

>>> d1 = Dice()
>>> d1.roll()
>>> d1.total()
7
>>> d1.faces
(2, 5)
"""

test_example_1_8 = """
>>> d2 = Dice()
>>> d2.roll()
>>> d2.total()
4
>>> d2.hardway()
False
>>> d2.faces
(1, 3)
"""


# End of Using a class to encapsulate data and processing

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
