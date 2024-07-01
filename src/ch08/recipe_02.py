# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Separating concerns via multiple inheritance


# Subection: How to do it...

from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    """Superclass for cards"""
    rank: int
    suit: str

    def __str__(self) -> str:
        return f"{self.rank:2d} {self.suit}"

class AceCard(Card):
    def __str__(self) -> str:
        return f" A {self.suit}"

class FaceCard(Card):
    def __str__(self) -> str:
        names = {11: "J", 12: "Q", 13: "K"}
        return f" {names[self.rank]} {self.suit}"

from typing import Protocol

class PointedCard(Protocol):
    rank: int
    def points(self) -> int:
        ...

class CribbagePoints(PointedCard):
    def points(self) -> int:
        return self.rank

class CribbageFacePoints(PointedCard):
    def points(self) -> int:
        return 10

class CribbageCard(Card, CribbagePoints):
    pass

class CribbageAce(AceCard, CribbagePoints):
    pass

class CribbageFace(FaceCard, CribbageFacePoints):
    pass

def make_cribbage_card(rank: int, suit: str) -> Card:
    if rank == 1:
        return CribbageAce(rank, suit)
    elif 2 <= rank < 11:
        return CribbageCard(rank, suit)
    elif 11 <= rank:
        return CribbageFace(rank, suit)
    else:
        raise ValueError(f"invalid rank {rank}")

test_example_1_8 = """
>>> import random
>>> random.seed(1)
>>> deck = [make_cribbage_card(rank+1, suit) for rank in range(13) for suit in  SUITS]
>>> random.shuffle(deck)
>>> len(deck)
52

>>> [str(c) for c in deck[:5]]
[' K ♡', ' 3 ♡', '10 ♡', ' 6 ♢', ' A ♢']

>>> sum(c.points() for c in deck[:5])
30
"""

# Subection: How it works...


test_example_2_1 = """
>>> import random
>>> random.seed(1)
>>> deck = [make_cribbage_card(rank+1, suit) for rank in range(13) for suit in  SUITS]
>>> random.shuffle(deck)

>>> c = deck[5]
>>> str(c)
'10 ♢'

>>> c.__class__.__name__
'CribbageCard'

>>> from pprint import pprint
>>> pprint(c.__class__.mro())
[<class 'recipe_02.CribbageCard'>,
 <class 'recipe_02.Card'>,
 <class 'recipe_02.CribbagePoints'>,
 <class 'recipe_02.PointedCard'>,
 <class 'typing.Protocol'>,
 <class 'typing.Generic'>,
 <class 'object'>]
"""

# Subection: There's more...

import logging

class Logged(Card, PointedCard):
    def __init__(self, rank: int, suit: str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(rank, suit)

    def points(self) -> int:
        p = super().points()  # type: ignore [safe-super]
        self.logger.debug("points {0}", p)
        return p

class LoggedCribbageAce(Logged, AceCard, CribbagePoints):
    pass

class LoggedCribbageCard(Logged, Card, CribbagePoints):
    pass

class LoggedCribbageFace(Logged, FaceCard, CribbageFacePoints):
    pass

def make_logged_card(rank: int, suit: str) -> Card:
    if rank == 1:
        return LoggedCribbageAce(rank, suit)
    elif 2 <= rank < 11:
        return LoggedCribbageCard(rank, suit)
    elif 11 <= rank:
        return LoggedCribbageFace(rank, suit)
    else:
        raise ValueError(f"invalid rank {rank!r}")

SUITS = '♠♡♢♣'

test_example_3_4 = """
>>> deck = [make_logged_card(rank+1, suit)
...     for rank in range(13)
...         for suit in SUITS]
>>> len(deck)
52
"""


# End of Separating concerns via multiple inheritance

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
