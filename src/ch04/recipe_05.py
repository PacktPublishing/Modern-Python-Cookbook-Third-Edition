# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 1: Lists and Sets
# Recipe: Writing list-related type hints


# Subsection: Getting ready

scheme = [
(' Brick_Red', (198, 45, 66)),
(' color1', (198.00, 100.50, 45.00)),
(' color2', (198.00, 45.00, 142.50)),
]
def hexify(r: float, g: float, b: float) -> str:
    return f'#{int(r) << 16 | int(g) << 8 | int(b):06X}'

test_example_1_3 = """
>>> hexify(198, 45, 66)
'#C62D42'
"""

# def source_to_hex_0(src):  # type: ignore [no-untyped-def]
#     return [
#         (n, hexify(*color)) for n, color in src
#     ]

# Subsection: How to do it...

ColorCode = tuple[str, str]
ColorCodeList = list[ColorCode]

from typing import Union
RGB_I = tuple[int, int, int]
RGB_F = tuple[float, float, float]
ColorRGB = tuple[str, Union[RGB_I, RGB_F]]
ColorRGBList = list[ColorRGB]
def source_to_hex(src: ColorRGBList) -> ColorCodeList:
    return [
        (n, hexify(*color)) for n, color in src
    ]

# Subsection: How it works...

list[tuple[str, Union[tuple[int, int, int], tuple[float, float, float]]]]


# End of Writing list-related type hints

test_source_to_hex = """
>>> scheme = [
... (' Brick_Red', (198, 45, 66)),
... (' color1', (198.00, 100.50, 45.00)),
... (' color2', (198.00, 45.00, 142.50)),
... ]
>>> source_to_hex(scheme)
[(' Brick_Red', '#C62D42'), (' color1', '#C6642D'), (' color2', '#C62D8E')]
"""


__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
