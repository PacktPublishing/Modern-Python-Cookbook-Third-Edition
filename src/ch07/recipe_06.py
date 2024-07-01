# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Using frozen dataclasses for immutable objects


# Subection: How to do it...

from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Card:
    rank: int
    suit: str

test_example_1_4 = """
>>> eight_hearts = Card(rank=8, suit='\N{White Heart Suit}')

>>> eight_hearts
Card(rank=8, suit='♡')

>>> eight_hearts.rank
8

>>> eight_hearts.suit
'♡'

>>> eight_hearts.suit = '\N{Black Spade Suit}'
Traceback (most recent call last):
...
dataclasses.FrozenInstanceError: cannot assign to field 'suit'
"""

# Subection: There's more...


from typing import NamedTuple
class CardT(NamedTuple):
    rank: int
    suit: str

class CardPoints(CardT):
    def points(self) -> int:
        if 1 <= self.rank < 10:
            return self.rank
        else:
            return 10

from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Hand:
    cards: list[CardPoints] = field(default_factory=list)

test_example_2_2 = """
>>> cards = [
... CardPoints(rank=3, suit='\N{WHITE DIAMOND SUIT}'),
... CardPoints(rank=6, suit='\N{BLACK SPADE SUIT}'),
... CardPoints(rank=7, suit='\N{WHITE DIAMOND SUIT}'),
... CardPoints(rank=1, suit='\N{BLACK SPADE SUIT}'),
... CardPoints(rank=6, suit='\N{WHITE DIAMOND SUIT}'),
... CardPoints(rank=10, suit='\N{WHITE HEART SUIT}')]
>>>
>>> h = Hand(cards)

>>> crib = Hand()
>>> d3 = CardPoints(rank=3, suit='\N{WHITE DIAMOND SUIT}')
>>> h.cards.remove(d3)
>>> crib.cards.append(d3)

>>> from pprint import pprint
>>> pprint(crib)
Hand(cards=[CardPoints(rank=3, suit='♢')])

>>> pprint(h)
Hand(cards=[CardPoints(rank=6, suit='♠'),
            CardPoints(rank=7, suit='♢'),
            CardPoints(rank=1, suit='♠'),
            CardPoints(rank=6, suit='♢'),
            CardPoints(rank=10, suit='♡')])
"""


# End of Using frozen dataclasses for immutable objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
