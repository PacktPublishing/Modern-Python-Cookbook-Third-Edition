# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 1: Lists and Sets
# Recipe: Writing list-related type hints

def hexify(r: float, g: float, b: float) -> str:
    return f'#{int(r) << 16 | int(g) << 8 | int(b):06X}'

def source_to_hex_0(src):
    return [
        (n, hexify(*color)) for n, color in src
    ]
