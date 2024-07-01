# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Deleting from a list of complicated objects


# Subection: Getting ready


test_example_1_1 = """
>>> song_list = [
... {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
... {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
... {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
... {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
... {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
... {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
... {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]
"""


from typing import TypedDict

class SongType(TypedDict):
    title: str
    writer: list[str]
    time: str

test_example_1_3 = """
>>> song_list = [
... {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
... {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
... {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
... {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
... {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
... {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
... {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]

>>> for item in song_list:
...     if 'Lake' in item['writer']:
...         print("remove", item['title'])
remove Stones of Years
remove Mass
remove Battlefield
"""


def naive_delete(data: list[SongType], writer: str) -> None:
    for index in range(len(data)):
        if 'Lake' in data[index]['writer']:
            del data[index]

test_example_1_5 = """
>>> song_list = [
... {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
... {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
... {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
... {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
... {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
... {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
... {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]

>>> naive_delete(song_list, 'Lake')
Traceback (most recent call last):
...
IndexError: list index out of range
"""

test_example_1_6 = """
>>> song_list = [
... {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
... {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
... {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
... {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
... {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
... {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
... {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]

>>> remove = list(filter(lambda x: 'Lake' in x['writer'], song_list))
>>> for x in remove:
...     song_list.remove(x)
>>> song_list
[{'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'}, {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'}, {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'}, {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}]
"""

def index_of_writer(data: list[SongType], writer: str) -> int | None:
    for i in range(len(data)):
        if writer in data[i]['writer']:
            return i
    return None

def multi_search_delete(data: list[SongType], writer: str) -> None:
    while (position := index_of_writer(data, 'Lake')) is not None:
        del data[position]  # or data.pop(position)

test_example_1_9 = """
>>> song_list = [
... {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
... {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
... {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
... {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
... {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
... {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
... {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]

>>> multi_search_delete(song_list, 'Lake')
>>> song_list
[{'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'}, {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'}, {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'}, {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}]
"""

# Subection: How to do it...

def incremental_delete(
    data: list[SongType],
    writer: str
) -> None:
    i = 0
    while i != len(data):
        if 'Lake' in data[i]['writer']:
            del data[i]
        else:
            i += 1

# Subection: There's more...

test_example_3_1 = """
>>> song_list = [
... {'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'},
... {'title': 'Stones of Years', 'writer': ['Emerson', 'Lake'], 'time': '3:43'},
... {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'},
... {'title': 'Mass', 'writer': ['Emerson', 'Lake'], 'time': '3:09'},
... {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'},
... {'title': 'Battlefield', 'writer': ['Lake'], 'time': '3:57'},
... {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}
... ]

>>> [item
...     for item in song_list
...         if 'Lake' not in item['writer']
... ]
[{'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'}, {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'}, {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'}, {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}]

>>> list(
...     filter(
...         lambda item: 'Lake' not in item['writer'],
...         song_list
...     )
... )
[{'title': 'Eruption', 'writer': ['Emerson'], 'time': '2:43'}, {'title': 'Iconoclast', 'writer': ['Emerson'], 'time': '1:16'}, {'title': 'Manticore', 'writer': ['Emerson'], 'time': '1:49'}, {'title': 'Aquatarkus', 'writer': ['Emerson'], 'time': '3:54'}]
"""


# End of Deleting from a list of complicated objects

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
