# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Making shallow and deep copies of objects


snippet_1_1 = """
b = object()
a = b
"""

# Subsection: Getting ready

test_example_2_1 = """
>>> some_dict = {'a': [1, 1, 2, 3]}
>>> another_dict = some_dict.copy()


>>> another_dict
{'a': [1, 1, 2, 3]}


>>> some_dict['a'].append(5)
>>> another_dict
{'a': [1, 1, 2, 3, 5]}


>>> id(some_dict['a']) == id(another_dict['a'])
True
"""


test_example_2_2 = """
>>> some_list = [[2, 3, 5], [7, 11, 13]]
>>> another_list = some_list.copy()
>>> some_list is another_list
False
>>> some_list[0] is another_list[0]
True
"""

# Subsection: How to do it...

test_example_3_1 = """
>>> import copy

>>> some_dict = {'a': [1, 1, 2, 3]}
>>> another_dict = copy.deepcopy(some_dict)

>>> some_dict['a'].append(5)
>>> some_dict
{'a': [1, 1, 2, 3, 5]}
>>> another_dict
{'a': [1, 1, 2, 3]}

>>> id(some_dict['a']) == id(another_dict['a'])
False
"""

# Subsection: How it works...

test_example_4_1 = """
>>> some_list = ([2, 3, 5], [7, 11, 13])
>>> some_dict = {'a': [1, 1, 2, 3]}

>>> copy_of_list = [item for item in some_list]
>>> copy_of_dict = {key:value for key, value in some_dict.items()}
"""

from typing import Any

def deepcopy_json(some_obj: Any) -> Any:
    match some_obj:
        case int() | float() | tuple() | str() | bytes() | None:
            return some_obj
        case list() as some_list:
            list_copy: list[Any] = []
            for item in some_list:
                list_copy.append(deepcopy_json(item))
            return list_copy
        case dict() as some_dict:
            dict_copy: dict[Any, Any] = {}
            for key in some_dict:
                dict_copy[key] = deepcopy_json(some_dict[key])
            return dict_copy
        case _:
            raise ValueError(f"can't copy {type(some_obj)}")


test_example_4_2 = """
>>> some_list = [[2, 3, 5], [7, 11, 13]]
>>> another = deepcopy_json(some_list)
>>> some_list == another
True
>>> some_list is another
False

>>> json_doc = [{'a': [1, 2], 'b': [3, 4]}]
>>> json_doc_2 = deepcopy_json(json_doc)
>>> json_doc_2 == json_doc
True
>>> json_doc_2 is json_doc
False
"""

# End of Making shallow and deep copies of objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
