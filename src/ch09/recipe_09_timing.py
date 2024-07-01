# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Simplifying complex algorithms with immutable data structures

# subsection: How it works...

import timeit
from textwrap import dedent

tuple_runtime = timeit.timeit(
    """list(rank_by_y(data))""",
    dedent("""
        from recipe_09 import text_parse, cleanse, rank_by_y, text_1
        data = cleanse(text_parse(text_1))
    """),
)
print(f"tuple {tuple_runtime}")
