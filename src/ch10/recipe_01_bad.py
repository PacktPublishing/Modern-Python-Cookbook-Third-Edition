# Python Cookbook, 3rd Ed.
#
# Chapter: Working with Type Matching and Annotations
# Recipe: Designing with type hints


from pathlib import Path


def datafile_iter(base):
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
            yield (path.relative_to(data), used_by)
        else:
            yield path.relative_to(data)


from typing import NamedTuple
class Referenced(NamedTuple):
    datafile: Path
    recipes: list[Path]

from collections.abc import Iterator

def datafile_iter_2(base: Path) -> Iterator[Path | Referenced]:
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
 (PosixPath('Volvo Ocean Race.html'), [PosixPath('ch11/recipe_08.py')]),
 PosixPath('anscombe.json'),
 (PosixPath('binned.csv'),
  [PosixPath('ch07/recipe_10.py'),
   PosixPath('ch07/recipe_03.py'),
   PosixPath('ch11/recipe_01.py')]),
...
 (PosixPath('y2.md'), [PosixPath('ch14/recipe_02.py')])]


"""

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}

