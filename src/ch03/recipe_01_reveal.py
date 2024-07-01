# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Function parameters and type hints

from typing import reveal_type

def hex2rgb(hx_int: int | str) -> tuple[int, int, int]:
    if isinstance(hx_int, str):
        if hx_int[0] == "#":
            hx_int = int(hx_int[1:], 16)
        else:
            hx_int = int(hx_int, 16)

    reveal_type(hx_int)  # Only used by mypy. Must be removed.

    r, g, b = (hx_int >> 16) & 0xff, (hx_int >> 8) & 0xff, hx_int & 0xff
    return r, g, b
