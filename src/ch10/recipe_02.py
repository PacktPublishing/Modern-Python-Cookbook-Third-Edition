# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Using the built-in type matching functions

from abc import abstractmethod

class Card:
    def __init__(self, rank: int, suit: str) -> None:
        self.rank = rank
        self.suit = suit
    @abstractmethod
    def __str__(self) -> str:
        ...
    @abstractmethod
    def points(self) -> int:
        ...

class AceCard(Card):
    def points(self) -> int:
        return 1
    def __str__(self) -> str:
        return f" A {self.suit}"

class NumberCard(Card):
    def points(self) -> int:
        return self.rank
    def __str__(self) -> str:
        return f"{self.rank:2d} {self.suit}"

class FaceCard(Card):
    def points(self) -> int:
        return 10
    def __str__(self) -> str:
        r = {11: "J", 12: "Q", 13: "K"}
        return f" {r[self.rank]} {self.suit}"

test_card = """
>>> a = AceCard(1, "\N{BLACK SPADE SUIT}")
>>> print(a)
 A ♠
>>> a.points()
1
"""


from pathlib import Path
from dataclasses import dataclass

@dataclass
class Referenced:
    """Defines a data file and applications that reference it."""
    datafile: Path
    recipes: list[Path]

from typing import TypeAlias

Unreferenced: TypeAlias = Path


from collections.abc import Iterator
DataFileIter: TypeAlias = Iterator[Unreferenced | Referenced]

def datafile_iter(base: Path) -> DataFileIter:
    data = (base / "data")
    code = (base / "src")
    for path in sorted(data.glob("*.*")):
        if not path.is_file():
            continue

        used_by = [
            chap_recipe.relative_to(code)
            for chap_recipe in code.glob("**/*.py")
            if (
                chap_recipe.is_file()
                and all(n not in chap_recipe.parts for n in ("__pycache__", "ch10", ".venv"))
                # and "ch10" not in chap_recipe.parts
                and path.name in chap_recipe.read_text()
            )
        ]

        if used_by:
            yield Referenced(path.relative_to(data), used_by)
        else:
            yield path.relative_to(data)


from collections.abc import Iterable

def analysis(source: Iterable[Unreferenced | Referenced]) -> None:
    good_files: list[Referenced] = []
    for file in source:
        if isinstance(file, Unreferenced):
            print(f"delete {file}")
        elif isinstance(file, Referenced):
            good_files.append(file)
        else:
            raise ValueError(f"unexpected type {type(file)}")
    print(f"Keep {len(good_files)} files")


test_analysis = """
>>> base = Path.cwd()
>>> all_usage = list(datafile_iter(base))
>>> df = datafile_iter(base)
>>> analysis(df)
delete Lew.dat
delete NEGIZ4.DAT
...
Keep 30 files
"""


from typing import cast


class Deck:
    def __init__(self, *cards: Card) -> None:
        self.cards = list(cards)
    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

class PokerDeck(Deck):
    pass

class PokerAce(AceCard):
    pass

class PokerFace(FaceCard):
    pass

class PokerCard(NumberCard):
    pass

class CribbageDeck(Deck):
    pass

class CribbageNumber(NumberCard):
    pass

class CribbageFace(FaceCard):
    pass

class InvalidCard(Card):
    def __init__(self, rank: int, suit: str) -> None:
        raise ValueError(f'invalid {rank} {suit}')



def make_deck(deck_class: type[Deck]) -> Deck:
    SUITS = (
        '\N{Black Club Suit}', '\N{White Diamond Suit}',
        '\N{White Heart Suit}', '\N{Black Spade Suit}')
    ace: type[Card]
    number: type[Card]
    face: type[Card]

    if issubclass(deck_class, PokerDeck):
        ace, number, face = PokerAce, PokerCard, PokerFace
    elif issubclass(deck_class, CribbageDeck):
        ace, number, face = CribbageNumber, CribbageNumber, CribbageFace
    else:
        raise ValueError(f"unexpected type {deck_class}")

    class_map = cast(list[type[Card]], (
        [InvalidCard, ace] + 9 * [number] + 3 * [face]
    ))

    deck = deck_class(
        *(class_map[rank](rank, suit)
          for rank in range(1, 14)
          for suit in SUITS
          )
    )
    return deck

test_make_deck = """
>>> p = make_deck(PokerDeck)
>>> p.cards[0]
<recipe_02.PokerAce object at ...>
>>> str(p.cards[0])
' A ♣'
"""


test_type_statement_problem = """
>>> import sys
>>> sys.version
'3.12.0 | packaged by conda-forge | (main, Oct  3 2023, 08:43:38) [Clang 15.0.7 ]'

>>> type Unreferenced = Path
>>> x = Path("somewhere")
>>> isinstance(x, Unreferenced)
Traceback (most recent call last):
...
TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union

"""

test_type_alias = """
>>> Unreferenced: TypeAlias = Path
>>> x = Path("somewhere")
>>> isinstance(x, Unreferenced)
True
"""



__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
