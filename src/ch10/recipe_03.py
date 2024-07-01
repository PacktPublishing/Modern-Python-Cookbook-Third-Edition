# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Using the match statement


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
        match file:
            case Unreferenced() as unref:
                print(f"delete {unref}")
            case Referenced() as ref:
                good_files.append(file)
            case _:
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


def analysis_2(source: Iterable[Unreferenced | Referenced]) -> None:
    good_files: list[Referenced] = []
    for file in source:
        match file:
            case Unreferenced() as unref:
                print(f"delete {unref}")
            case Referenced(_, [Path()]) as single:
                print(f"single use: {single}")
                good_files.append(single)
            case Referenced() as multiple:
                good_files.append(multiple)
            case _:
                raise ValueError(f"unexpected type {type(file)}")
    print(f"Keep {len(good_files)} files")

test_analysis_2 = """
>>> base = Path.cwd()
>>> all_usage = list(datafile_iter(base))
>>> df = datafile_iter(base)
>>> analysis_2(df)
delete Lew.dat
delete NEGIZ4.DAT
single use: Referenced(datafile=PosixPath('Volvo Ocean Race.html'), recipes=[PosixPath('ch11/recipe_08.py')])
...
single use: Referenced(datafile=PosixPath('race_result.json'), recipes=[PosixPath('ch11/recipe_06.py')])
...
Keep 30 files
"""



from recipe_02 import Card, AceCard, FaceCard, NumberCard
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
<recipe_03.PokerAce object at ...>
>>> str(p.cards[0])
' A ♣'
"""


__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
