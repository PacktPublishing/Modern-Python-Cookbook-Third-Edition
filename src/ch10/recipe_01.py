# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Designing with type hints


from pathlib import Path
from dataclasses import dataclass

@dataclass
class Referenced:
    """Defines a data file and applications that reference it."""
    datafile: Path
    recipes: list[Path]

from typing import TypeAlias

Unreferenced: TypeAlias = Path

ContentType: TypeAlias = Unreferenced | Referenced

from collections.abc import Iterator

def datafile_iter(base: Path) -> Iterator[ContentType]:
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
                and "__pycache__" not in chap_recipe.parts
                and ".venv" not in chap_recipe.parts
                and "ch10" not in chap_recipe.parts
                and path.name in chap_recipe.read_text()
            )
        ]

        if used_by:
            yield Referenced(path.relative_to(data), used_by)
        else:
            yield path.relative_to(data)

test_example_1 = """
>>> base = Path.cwd()
>>> all_usage = list(datafile_iter(base))
>>> from pprint import pprint
>>> pprint(all_usage)
[PosixPath('Lew.dat'),
 PosixPath('NEGIZ4.DAT'),
 Referenced(datafile=PosixPath('Volvo Ocean Race.html'),
            recipes=[PosixPath('ch11/recipe_08.py')]),
 PosixPath('anscombe.json'),
 Referenced(datafile=PosixPath('binned.csv'),
            recipes=[PosixPath('ch07/recipe_10.py'),
                     PosixPath('ch07/recipe_03.py'),
                     PosixPath('ch11/recipe_01.py')]),
...
 Referenced(datafile=PosixPath('y2.md'),
            recipes=[PosixPath('ch14/recipe_02.py')])]

"""


__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
