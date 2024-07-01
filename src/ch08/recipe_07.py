# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Improving performance with an ordered collection


# Subection: Getting ready

import bisect
from collections.abc import Iterable, Iterator
from typing import Any

from recipe_06 import PinochleCard, make_pinochle_deck, make_pinochle_card

# Subection: How to do it...

class Hand:
    def __init__(self, card_iter: Iterable[PinochleCard]) -> None:
        self.cards = list(card_iter)
        self.cards.sort()

    def add(self, aCard: PinochleCard) -> None:
        bisect.insort(self.cards, aCard)

    def index(self, aCard: PinochleCard) -> int:
        i = bisect.bisect_left(self.cards, aCard)
        if i != len(self.cards) and self.cards[i] == aCard:
            return i
        raise ValueError(f'card not found: {aCard}')

    def __contains__(self, aCard: PinochleCard) -> bool:
        try:
            self.index(aCard)
            return True
        except ValueError:
            return False

    def __iter__(self) -> Iterator[PinochleCard]:
        return iter(self.cards)

    def __le__(self, other: Any) -> bool:
        match other:
            case Hand():
                for card in self:
                    if card not in other:
                        return False  # Can't be a subset
                return True
            case _:
                raise TypeError(f'unexpected type {type(other)}: {other!r}')

test_example_2_7 = """
>>> import random
>>> random.seed(4)
>>> deck = make_pinochle_deck()
>>> random.shuffle(deck)
>>> h = Hand(deck[:12])
>>> [str(c) for c in h.cards]
[' 9 ♣', '10 ♣', ' J ♠', ' J ♢', ' J ♢', ' Q ♠', ' Q ♣', ' K ♠', ' K ♠', ' K ♣', ' A ♡', ' A ♣']


>>> pinochle = Hand([make_pinochle_card(11, '♢'), make_pinochle_card(12, '♠')])
>>> pinochle <= h
True


>>> sum(c.points() for c in h)
56
"""

# Subection: How it works...

from typing import TypeVar, TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import SupportsAllComparisons
    Sortable = TypeVar("Sortable", bound=SupportsAllComparisons)

def search(a: 'list[Sortable]', x: 'Sortable') -> int:
    lo, hi = 0, len(a)
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if x == a[mid]: return mid
        elif x < a[mid]: hi = mid
        else: lo = mid + 1
    return lo

test_search = """
>>> some_list = [1, 1, 2, 3, 5, 8, 13, 21]
>>> search(some_list, 3)
3
>>> search(some_list, 4)
3
"""

# End of Improving performance with an ordered collection

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
