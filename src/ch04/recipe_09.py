# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 1: Lists and Sets
# Recipe: Writing set-related type hints


# Subsection: Getting ready

from enum import Enum
import random

class Die(str, Enum):
    d_1 = "\u2680"
    d_2 = "\u2681"
    d_3 = "\u2682"
    d_4 = "\u2683"
    d_5 = "\u2684"
    d_6 = "\u2685"

def zonk(n: int = 6) -> tuple[Die, ...]:
    faces = list(Die)
    return tuple(random.choice(faces) for _ in range(n))


test_example_1_2 = """
>>> random.seed(42)
>>> zonk()
(<Die.d_6: '⚅'>, <Die.d_1: '⚀'>, <Die.d_1: '⚀'>, <Die.d_6: '⚅'>, <Die.d_3: '⚂'>, <Die.d_2: '⚁'>)

"""

# Subsection: How to do it...

import collections

def eval_zonk_6(hand: tuple[Die, ...]) -> str:
    assert len(hand) == 6, "Only works for 6-dice zonk."
    unique: set[Die] = set(hand)

    faces = list(Die)
    small_straights = [
        set(faces[:-1]), set(faces[1:])
    ]

    if len(unique) == 6:
        return "large straight"
    elif len(unique) == 5 and unique in small_straights:
        return "small straight"
    elif len(unique) == 2:
        return "three of a kind"
    elif len(unique) == 1:
        return "six of a kind"
    elif len(unique) in {3, 4}:
        # 4 unique: wwwxyz (good) or wwxxyz (bad)
        # 3 unique: xxxxyz, xxxyyz (good) or xxyyzz (bad)
        frequencies: set[int] = set(
            collections.Counter(hand).values())
        if 3 in frequencies or 4 in frequencies:
            return "three of a kind"
        elif Die.d_1 in unique:
            return "ace"
    return "Zonk!"


# End of Writing set-related type hints

test_zonk_6 = """
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_4, Die.d_5, Die.d_6])
'large straight'
>>> eval_zonk_6([Die.d_1, Die.d_2, Die.d_3, Die.d_4, Die.d_5, Die.d_1])
'small straight'
>>> eval_zonk_6([Die.d_6, Die.d_2, Die.d_3, Die.d_4, Die.d_5, Die.d_5])
'small straight'
>>> eval_zonk_6([Die.d_6, Die.d_6, Die.d_3, Die.d_4, Die.d_6, Die.d_5])
'three of a kind'
>>> eval_zonk_6([Die.d_6, Die.d_6, Die.d_6, Die.d_6, Die.d_6, Die.d_6])
'six of a kind'
>>> eval_zonk_6([Die.d_6, Die.d_6, Die.d_5, Die.d_5, Die.d_4, Die.d_1])
'ace'
>>> eval_zonk_6([Die.d_6, Die.d_6, Die.d_5, Die.d_5, Die.d_4, Die.d_4])
'Zonk!'

"""
__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
