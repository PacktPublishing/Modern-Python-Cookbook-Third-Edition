# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Using typing.NamedTuple for immutable objects


# Subection: How to do it...

from typing import NamedTuple
class Card(NamedTuple):
    rank: int
    suit: str

test_example_1_3 = """
>>> eight_hearts = Card(rank=8, suit='\N{White Heart Suit}')
>>> eight_hearts 
Card(rank=8, suit='♡')

>>> eight_hearts.rank
8

>> eight_hearts.suit
'♡'

>>> eight_hearts[0]
8

>>> eight_hearts.suit = '\N{Black Spade Suit}'
Traceback (most recent call last):
...
AttributeError: can't set attribute
"""

# Subection: There's more...

class CardPoints(NamedTuple):
    rank: int
    suit: str

    def points(self) -> int:
        if 1 <= self.rank < 10:
            return self.rank
        else:
            return 10


# End of Using typing.NamedTuple for immutable objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
