# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Creating a class that has orderable objects


# Subection: Getting ready

from recipe_02 import AceCard, Card, FaceCard, SUITS, PointedCard

class PinochlePoints(PointedCard):
    def points(self: PointedCard) -> int:
        _points = {9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 14: 11}
        return _points[self.rank]

# Subection: How to do it...

from typing import Protocol, Any

class CardLike(Protocol):
    rank: int
    suit: str

class SortableCard(CardLike):
    def __lt__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) < (other.rank, other.suit)
    def __le__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) <= (other.rank, other.suit)
    def __gt__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) > (other.rank, other.suit)
    def __ge__(self: CardLike, other: Any) -> bool:
        return (self.rank, self.suit) >= (other.rank, other.suit)

class PinochleAce(AceCard, SortableCard, PinochlePoints):
    pass

class PinochleFace(FaceCard, SortableCard, PinochlePoints):
    pass

class PinochleNumber(Card, SortableCard, PinochlePoints):
    pass

from typing import TypeAlias
PinochleCard: TypeAlias = PinochleAce | PinochleFace | PinochleNumber

def make_pinochle_card(rank: int, suit: str) -> PinochleCard:
    if rank in (9, 10):
        return PinochleNumber(rank, suit)
    elif rank in (11, 12, 13):
        return PinochleFace(rank, suit)
    else:
        return PinochleAce(rank, suit)

test_example_2_7 = """
>>> c1 = make_pinochle_card(9, '♡')
>>> c2 = make_pinochle_card(10, '♡')
>>> c1 < c2
True

>>> c1 == c1  # Cards match themselves
True

>>> c1 == c2
False

>>> c1 > c2
False
"""


def make_pinochle_deck() -> list[PinochleCard]:
    return [
        make_pinochle_card(r, s)
            for _ in range(2)
                for r in range(9, 15)
                    for s in SUITS
    ]

# Subection: How it works...


test_example_3_1 = """
>>> c1 = make_pinochle_card(9, '♡')
>>> c2 = make_pinochle_card(10, '♡')

>>> c1 <= c2
True
"""

test_example_3_2 = """
>>> deck = make_pinochle_deck()
>>> len(deck)
48

>>> [str(c) for c in deck[:8]]
[' 9 ♠', ' 9 ♡', ' 9 ♢', ' 9 ♣', '10 ♠', '10 ♡', '10 ♢', '10 ♣']

>>> [str(c) for c in deck[24:32]]
[' 9 ♠', ' 9 ♡', ' 9 ♢', ' 9 ♣', '10 ♠', '10 ♡', '10 ♢', '10 ♣']

>>> import random
>>> random.seed(4)
>>> random.shuffle(deck)
>>> [str(c) for c in sorted(deck[:12])]
[' 9 ♣', '10 ♣', ' J ♠', ' J ♢', ' J ♢', ' Q ♠', ' Q ♣', ' K ♠', ' K ♠', ' K ♣', ' A ♡', ' A ♣']
"""

# Subection: There's more...


test_example_4_1 = """
>>> c1 = make_pinochle_card(9, '♡')
>>> c1 <= 10
Traceback (most recent call last):
...
AttributeError: 'int' object has no attribute 'rank'
"""


def __lt__(self: CardLike, other: Any) -> bool:
    match other:
        case int() as rank:
            return self.rank < rank
        case CardLike() as card:
            return (self.rank, self.suit) < (card.rank, card.suit)
        case _:
            raise TypeError(f"unexpected type {type(other)} for {other}")


# End of Creating a class that has orderable objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
