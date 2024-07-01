# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Essential type hints for class definitions


# Subection: How to do it...

import random

class Dice:
    RNG = random.Random()
    def __init__(self, n: int, sides: int = 6) -> None:
        self.n_dice = n
        self.sides = sides
        self.faces: list[int]
        self.roll_number = 0
    def __str__(self) -> str:
        return ", ".join(
            f"{i}: {f}"
            for i, f in enumerate(self.faces)
        )

    def total(self) -> int:
        return sum(self.faces)

    def average(self) -> float:
        return sum(self.faces) / self.n_dice

    def first_roll(self) -> list[int]:
        self.roll_number = 0
        self.faces = [
            self.RNG.randint(1, self.sides)
            for _ in range(self.n_dice)
        ]
        return self.faces

    def reroll(self, positions: set[int]) -> list[int]:
        self.roll_number += 1
        for p in positions:
            self.faces[p] = self.RNG.randint(1, self.sides)
        return self.faces

# Subection: How it works...


test_roll = """
>>> d = Dice(6)
>>> d.RNG.seed(42)

>>> r1 = d.first_roll()
>>> r1
[6, 1, 1, 6, 3, 2]

"""

# End of Essential type hints for class definitions

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
