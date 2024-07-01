# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Writing recursive generator functions with the yield from statement


# subsection: Getting ready

document = {
    "field": "value1",
    "field2": "value",
    "array": [
        {"array_item_key1": "value"},
        {"array_item_key2": "array_item_value2"}
    ],
    "object": {
        "attribute1": "value",
        "attribute2": "value2"
    },
}


# subsection: How to do it...

from collections.abc import Iterator
from typing import Any, TypeAlias

JSON_DOC: TypeAlias = (
    None | str | int | float | bool | dict[str, Any] | list[Any]
)
Node_Id: TypeAlias = Any

def find_value_sketch(
    value: Any,
    node: JSON_DOC,
    path: list[Node_Id] | None = None
) -> Iterator[list[Node_Id]]:
    if path is None:
        path = []
    match node:
        case dict() as dnode:
            pass  # apply find_value to each key in dnode
        case list() as lnode:
            pass  # apply find_value to each item in lnode
        case _ as pnode: # str, int, float, bool, None
            if pnode == value:
                yield path

def find_value_y(
    value: Any,
    node: JSON_DOC,
    path: list[Node_Id] | None = None
) -> Iterator[list[Node_Id]]:
    if path is None:
        path = []
    match node:
        case dict() as dnode:
            for key in sorted(dnode.keys()):
                for match in find_value_y(value, dnode[key], path + [key]):
                    yield match
        case list() as lnode:
            for index in range(len(lnode)):
                for match in find_value_y(value, lnode[index], path + [index]):
                    yield match
        case _ as pnode:
            # str, int, float, bool, None
            if pnode == value:
                yield path

def find_value_yf(
    value: Any,
    node: JSON_DOC,
    path: list[Node_Id] | None = None
) -> Iterator[list[Node_Id]]:
    if path is None:
        path = []
    match node:
        case dict() as dnode:
            for key in sorted(dnode.keys()):
                yield from find_value_yf(value, dnode[key], path + [key])
        case list() as lnode:
            for index, item in enumerate(lnode):
                yield from find_value_yf(value, item, path + [index])
        case _ as pnode:
            # str, int, float, bool, None
            if pnode == value:
                yield path

def find_value(
    value: Any,
    node: JSON_DOC,
    path: list[Node_Id] | None = None
) -> Iterator[list[Node_Id]]:
    if path is None:
        path = []
    match node:
        case dict() as dnode:
            for key in sorted(dnode.keys()):
                yield from find_value(
                    value, node[key], path + [key])
        case list() as lnode:
            for index, item in enumerate(lnode):
                yield from find_value(
                    value, item, path + [index])
        case _ as pnode:
            # str, int, float, bool, None
            if pnode == value:
                yield path


test_example_2_7 = """
>>> list(find_value_y('array_item_value2', document))
[['array', 1, 'array_item_key2']]
>>> list(find_value_yf('array_item_value2', document))
[['array', 1, 'array_item_key2']]
>>> list(find_value('array_item_value2', document))
[['array', 1, 'array_item_key2']]
"""

test_example_2_8 = """
>>> places = list(find_value('value', document))
>>> places
[['array', 0, 'array_item_key1'], ['field2'], ['object', 'attribute1']]
"""

# subsection: How it works...

from collections.abc import Collection, Iterator
from typing import TypeVar

def test_yield() -> None:

    T = TypeVar("T")
    def some_function(x: Collection[T]) -> Iterator[T]:
        for item in x:
            yield item

    d = [1, 2, 3]
    assert list(some_function(d)) == d


# subsection: There's more...

import math

def factor_list(x: int) -> list[int]:
    limit = int(math.sqrt(x) + 1)
    for n in range(2, limit):
        q, r = divmod(x, n)
        if r == 0:
            return [n] + factor_list(q)
    return [x]


def factor_iter(x: int) -> Iterator[int]:
    limit = int(math.sqrt(x) + 1)
    for n in range(2, limit):
        q, r = divmod(x, n)
        if r == 0:
            yield n
            yield from factor_iter(q)
            return
    yield x

test_example_4_3 = """
>>> factor_list(384)
[2, 2, 2, 2, 2, 2, 2, 3]
>>> factor_list(42)
[2, 3, 7]

>>> from collections import Counter

>>> Counter(factor_iter(384))
Counter({2: 7, 3: 1})
"""


# End of Writing recursive generator functions with the yield from statement

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
