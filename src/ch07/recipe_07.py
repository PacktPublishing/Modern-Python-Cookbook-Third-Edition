# Python Cookbook, 3rd Ed.
#
# Chapter: Basics of Classes and Objects
# Recipe: Optimizing small objects with \_\_slots\_\_

import random
from typing import NamedTuple

class Card(NamedTuple):
    rank: int
    suit: str

class CardPoints(Card):
    def points(self) -> int:
        if 1 <= self.rank < 10:
            return self.rank
        return 10

class Deck(list[CardPoints]):
    SUITS = ('\N{Black Club Suit}', '\N{White Diamond Suit}', '\N{White Heart Suit}', '\N{Black Spade Suit}')
    def __init__(self) -> None:
        super().__init__(
            [
                CardPoints(r, s)
                for r in range(1, 15)
                    for s in self.SUITS]
        )
    def shuffle(self) -> None:
        random.shuffle(self)

from dataclasses import dataclass
@dataclass
class Player:
    name: str


class Hand(list[Card]):
    pass

# Subection: How to do it...

class Cribbage:
    __slots__ = ('deck', 'players', 'crib', 'dealer', 'opponent')
    def __init__(
            self,
            deck: Deck,
            player1: Player,
            player2: Player
    ) -> None:
        self.deck = deck
        self.players = [player1, player2]
        random.shuffle(self.players)
        self.dealer, self.opponent = self.players
        self.crib = Hand()

    def new_deal(self) -> None:
        self.deck.shuffle()
        self.players = list(reversed(self.players))
        self.dealer, self.opponent = self.players
        self.crib = Hand()

test_example_1_5 = """
>>> deck = Deck()
>>> c = Cribbage(deck, Player("1"), Player("2"))
>>> c.dealer
Player(name='2')
>>> c.opponent
Player(name='1')
>>> c.new_deal()
>>> c.dealer
Player(name='1')
>>> c.opponent
Player(name='2')
"""

test_example_1_6 = """
>>> deck = Deck()
>>> c = Cribbage(deck, Player("1"), Player("2"))

>>> c.some_other_attribute = True
Traceback (most recent call last):
...
AttributeError: 'Cribbage' object has no attribute 'some_other_attribute'
"""


# End of Optimizing small objects with \_\_slots\_\_

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
