# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Designing functions with optional parameters


# Subsection: How to do it...
# Topic: Particular to General design

import random

def die() -> int:
    return random.randint(1, 6)

def craps() -> tuple[int, int]:
    return (die(), die())

def zonk() -> tuple[int, ...]:
  return tuple(die() for x in range(6))

test_example_1 = """
>>> import random
>>> random.seed(42)
>>> zonk()
(6, 1, 1, 6, 3, 2)
"""

def craps_v2() -> tuple[int, ...]:
    return tuple(die() for x in range(2))

def dice_v2(n: int) -> tuple[int, ...]:
    return tuple(die() for x in range(n))

def dice_v3(n: int = 2) -> tuple[int, ...]:
    return tuple(die() for x in range(n))


# Subsection: How to do it...
# Topic: General to Particular design

def dice_d1(n):
    return tuple(die() for x in range(n))

def dice_d2(n=2):
    return tuple(die() for x in range(n))

def dice(n: int=2) -> tuple[int, ...]:
    return tuple(die() for x in range(n))


# Subsection: There's more...

def craps_v3():
    return dice(2)

def zonk_v3():
    return dice(6)



# End of Designing functions with optional parameters

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
