# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Leveraging Python's duck typing


# Subection: How to do it...

import random

class Dice1:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self.roll()
    def roll(self) -> tuple[int, ...]:
        self.dice = (
            self._rng.randint(1, 6),
            self._rng.randint(1, 6))
        return self.dice

import random

class Die:
    def __init__(self, rng: random.Random) -> None:
        self._rng = rng
    def roll(self) -> int:
        return self._rng.randint(1, 6)

class Dice2:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._dice = [Die(self._rng) for _ in range(2)]
        self.roll()
    def roll(self) -> tuple[int, ...]:
        self.dice = tuple(d.roll() for d in self._dice)
        return self.dice

from collections.abc import Iterator

def roller(
    dice_class: type[Dice1 | Dice2],
    seed: int | None = None,
    *,
    samples: int = 10
) -> Iterator[tuple[int, ...]]:
    dice = dice_class(seed)
    for _ in range(samples):
        yield dice.roll()

test_example_1_4 = """
>>> list(roller(Dice1, 1, samples=5))
[(1, 3), (1, 4), (4, 4), (6, 4), (2, 1)]

>>> list(roller(Dice2, 1, samples=5))
[(1, 3), (1, 4), (4, 4), (6, 4), (2, 1)]
"""

# Subection: There's more...

from typing import TypeAlias

DiceU: TypeAlias = Dice1 | Dice2


from typing import Protocol

class DiceP(Protocol):
    def roll(self) -> tuple[int, ...]:
        ...


# End of Leveraging Python's duck typing

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
