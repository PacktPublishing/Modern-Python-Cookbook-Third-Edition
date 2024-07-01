# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Function parameters and type hints


# Subsection: Getting ready

snippet = """
r, g, b = (hx_int >> 16) & 0xFF, (hx_int >> 8) & 0xFF, hx_int & 0xFF
"""

# Subsection: How to do it...

def hex2rgb_1(hx_int):
    if isinstance(hx_int, str):
        if hx_int[0] == "#":
            hx_int = int(hx_int [1:], 16)
        else:
            hx_int = int(hx_int, 16)
    r, g, b = (hx_int >> 16) & 0xff, (hx_int >> 8) & 0xff, hx_int & 0xff
    return r, g, b

def hex2rgb(hx_int: int | str) -> tuple[int, int, int]:
    if isinstance(hx_int, str):
        if hx_int[0] == "#":
            hx_int = int(hx_int[1:], 16)
        else:
            hx_int = int(hx_int, 16)
    r, g, b = (hx_int >> 16) & 0xff, (hx_int >> 8) & 0xff, hx_int & 0xff
    return r, g, b


# Subsection: How it works...


# Subsection: There's more...

def rgb_to_hsl_t(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    ...
    return 0.0, 0.0, 0.0  # placeholder for mypy

def hsl_comp_t(hsl: tuple[float, float, float]) -> tuple[float, float, float]:
    ...
    return 0.0, 0.0, 0.0  # placeholder for mypy

def hsl_to_rgb_t(hsl: tuple[float, float, float]) -> tuple[int, int, int]:
    ...
    return 0, 0, 0  # placeholder for mypy


from typing import TypeAlias

RGB_a: TypeAlias = tuple[int, int, int]

HSL_a: TypeAlias = tuple[float, float, float]

def rgb_to_hsl(color: RGB_a) -> HSL_a:
    ...
    return 0.0, 0.0, 0.0  # placeholder for mypy

def hsl_complement(color: HSL_a) -> HSL_a:
    ...
    return 0.0, 0.0, 0.0  # placeholder for mypy

def hsl_to_rgb(color: HSL_a) -> RGB_a:
    ...
    return 0, 0, 0  # placeholder for mypy


from typing import NamedTuple

class RGB(NamedTuple):
    red: int
    green: int
    blue: int

def hex_to_rgb2(hx_int: int | str) -> RGB:
    if isinstance(hx_int, str):
        if hx_int[0] == "#":
            hx_int = int(hx_int[1:], 16)
        else:
            hx_int = int(hx_int, 16)

    # reveal_type(hx_int)

    return RGB(
      (hx_int >> 16) & 0xff,
      (hx_int >> 8) & 0xff,
      (hx_int & 0xff)
    )



# End of Function parameters and type hints

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
