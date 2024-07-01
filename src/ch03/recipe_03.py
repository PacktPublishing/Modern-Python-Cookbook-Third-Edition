# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Designing type hints for optional parameters


# Subsection: How to do it...
import random

def dice(n, sides=6):
    return tuple(random.randint(1, sides) for _ in range(n))

def dice_t(n: int, sides: int = 6) -> tuple[int, ...]:
    return tuple(random.randint(1, sides) for _ in range(n))


# Subsection: How it works...

Pi: float = 355/113


# Subsection: There's more...

def polydice(n: int | None = None, sides: int = 6) -> tuple[int, ...]:

    if n is None:
        n = 2 if sides == 6 else 1

    return tuple(random.randint(1, sides) for _ in range(n))

test_example_1 = """
>>> import random
>>> random.seed(113)
>>> polydice()
(1, 6)

>>> polydice(6)
(6, 3, 1, 4, 5, 3)

>>> polydice(sides=8)
(4,)

>>> polydice(n=8, sides=4)
(4, 1, 1, 3, 2, 3, 4, 3)
"""

snippet = """
n_dice = n or 2 if sides == 6 else 1
"""


# End of Designing type hints for optional parameters

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
