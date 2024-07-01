# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Choosing between inheritance and composition -- the "is-a" question


# Subection: Getting ready

from typing import NamedTuple

class Card(NamedTuple):
    rank: int
    suit: str

Spades, Hearts, Diamonds, Clubs = ('\u2660', '\u2661', '\u2662', '\u2663')


test_example_1_2 = """
>>> Card(2, Spades)
Card(rank=2, suit='♠')
"""

# Subection: How to do it...
# Topic: Wrapping -- aggregation and composition


test_example_2_1 = """
>>> domain = list(
...     Card(r+1,s)
...         for r in range(13)
...             for s in (Spades, Hearts, Diamonds, Clubs)
... )
"""


import random

class Deck_W:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self.deal_iter = iter(self.cards)

    def shuffle(self) -> None:
        random.shuffle(self.cards)
        self.deal_iter = iter(self.cards)

    def deal(self) -> Card:
        return next(self.deal_iter)

test_example_2_5 = """
>>> domain = list(
...     Card(r+1,s)
...         for r in range(13)
...             for s in (Spades, Hearts, Diamonds, Clubs)
... )
>>> len(domain)
52

>>> d = Deck_W(domain)

>>> import random
>>> random.seed(1)
>>> d.shuffle()
>>> [d.deal() for _ in range(5)]
[Card(rank=13, suit='♡'), Card(rank=3, suit='♡'), Card(rank=10, suit='♡'), Card(rank=6, suit='♢'), Card(rank=1, suit='♢')]
"""

# Subection: How to do it...
# Topic: Extending -- inheritance

class Deck_X(list[Card]):
    def shuffle(self) -> None:
        random.shuffle(self)
        self.deal_iter = iter(self)

    def deal(self) -> Card:
        return next(self.deal_iter)

test_example_3_3 = """
>>> dx = Deck_X(
... Card(r+1,s)
...     for r in range(13)
...         for s in (Spades, Hearts, Diamonds, Clubs)
... )
>>> len(dx)
52

>>> import random
>>> random.seed(1)
>>> dx.shuffle()
>>> [dx.deal() for _ in range(5)]
[Card(rank=13, suit='♡'), Card(rank=3, suit='♡'), Card(rank=10, suit='♡'), Card(rank=6, suit='♢'), Card(rank=1, suit='♢')]
"""

# Subection: How it works...

class Parent:
    def some_method(self) -> None:
        return None

class SomeClass(Parent):
    def some_method(self) -> None:
        # do something extra
        super().some_method()

# Subection: There's more...


test_example_5_1 = """
>>> c_2s = Card(2, Spades)
>>> c_2s
Card(rank=2, suit='♠')

>>> another = c_2s
>>> another
Card(rank=2, suit='♠')

>>> id(c_2s) == id(another)
True

>>> c_2s is another
True
"""


# End of Choosing between inheritance and composition -- the "is-a" question

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
