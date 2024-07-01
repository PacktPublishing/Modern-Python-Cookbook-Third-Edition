# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Using dataclasses for mutable objects


# Subection: How to do it...

from typing import NamedTuple
class Card(NamedTuple):
    rank: int
    suit: str

class CardPoints(Card):
    def points(self) -> int:
        if 1 <= self.rank < 10:
            return self.rank
        else:
            return 10

from dataclasses import dataclass

@dataclass
class CribbageHand:
    cards: list[CardPoints]

    def to_crib(self, card1: CardPoints, card2: CardPoints) -> None:
        self.cards.remove(card1)
        self.cards.remove(card2)

test_example_1_6 = """
>>> cards = [
... CardPoints(rank=3, suit='\N{WHITE DIAMOND SUIT}'),
... CardPoints(rank=6, suit='\N{BLACK SPADE SUIT}'),
... CardPoints(rank=7, suit='\N{WHITE DIAMOND SUIT}'),
... CardPoints(rank=1, suit='\N{BLACK SPADE SUIT}'),
... CardPoints(rank=6, suit='\N{WHITE DIAMOND SUIT}'),
... CardPoints(rank=10, suit='\N{WHITE HEART SUIT}')]
>>> ch1 = CribbageHand(cards)

>>> from pprint import pprint
>>> pprint(ch1)
CribbageHand(cards=[CardPoints(rank=3, suit='♢'),
                    CardPoints(rank=6, suit='♠'),
                    CardPoints(rank=7, suit='♢'),
                    CardPoints(rank=1, suit='♠'),
                    CardPoints(rank=6, suit='♢'),
                    CardPoints(rank=10, suit='♡')])

>>> [c.points() for c in ch1.cards]
[3, 6, 7, 1, 6, 10]


>>> ch1.to_crib(
...     CardPoints(rank=3, suit='\N{WHITE DIAMOND SUIT}'), 
...     CardPoints(rank=1, suit='\N{BLACK SPADE SUIT}'))

>>> pprint(ch1)
CribbageHand(cards=[CardPoints(rank=6, suit='♠'),
                    CardPoints(rank=7, suit='♢'),
                    CardPoints(rank=6, suit='♢'),
                    CardPoints(rank=10, suit='♡')])

>>> [c.points() for c in ch1.cards]
[6, 7, 6, 10]
"""

# Subection: There's more...

import random

from typing import ClassVar

@dataclass(init=False)
class Deck:
    SUITS: ClassVar[tuple[str, ...]] = (
    '\N{Black Club Suit}',
    '\N{White Diamond Suit}',
    '\N{White Heart Suit}',
    '\N{Black Spade Suit}'
    )

    cards: list[CardPoints]

    def __init__(self) -> None:
        self.cards = [
            CardPoints(rank=r, suit=s)
            for r in range(1, 14)
                for s in self.SUITS
        ]
        random.shuffle(self.cards)


# End of Using dataclasses for mutable objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
