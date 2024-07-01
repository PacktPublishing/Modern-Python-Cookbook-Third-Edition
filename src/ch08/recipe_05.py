# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Using more complex structures -- maps of lists


# Subection: Getting ready

log_data = """
[2016-04-24 11:05:01,462] INFO in module1: Sample Message One
[2016-04-24 11:06:02,624] DEBUG in module2: Debugging
[2016-04-24 11:07:03,246] WARNING in module1: Something might have gone wrong
"""

import re
from typing import NamedTuple

class Event(NamedTuple):
    timestamp: str
    level: str
    module: str
    message: str

    @staticmethod
    def from_line(line: str) -> 'Event | None':
        pattern = re.compile(
            r"\[(?P<timestamp>.*?)\]\s+"
            r"(?P<level>\w+)\s+"
            r"in\s+(?P<module>\w+)"
            r":\s+(?P<message>.*)"
            )
        if log_line := pattern.match(line):
            return Event(**log_line.groupdict())
        else:
            return None

test_example_1_3 = """
>>> Event.from_line(
...     "[2016-04-24 11:05:01,462] INFO in module1: Sample Message One")
Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One')

>>> list(Event.from_line(l) for l in log_data.splitlines())
[None, Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'), Event(timestamp='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging'), Event(timestamp='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')]

"""

code_snippet_1_4 = """
>>> pprint(summary)
{'module1': [
   Event('2016-04-24 11:05:01,462', 'INFO', 'module1', 'Sample Message One'),
   Event('2016-04-24 11:07:03,246', 'WARNING', 'module1', 'Something might have gone wrong')],
 'module2': [
   Event('2016-04-24 11:06:02,624', 'DEBUG', 'module2', 'Debugging')]
}
"""

# Subection: How to do it...

from collections import defaultdict
from collections.abc import Iterable

from typing import TypeAlias
Summary: TypeAlias = defaultdict[str, list[Event]]

def summarize(data: Iterable[Event]) -> Summary:
    module_details: Summary = defaultdict(list)
    for event in data:
        module_details[event.module].append(event)
    return module_details

test_example_2_6 = """
>>> event_none_iter = (Event.from_line(l) for l in log_data.splitlines())
>>> event_iter = filter(None, event_none_iter)
>>> summary = summarize(event_iter)
>>> from pprint import pprint
>>> pprint(summary)
defaultdict(<class 'list'>,
            {'module1': [Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'),
                         Event(timestamp='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')],
             'module2': [Event(timestamp='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')]})
"""

# Subection: There's more...

class ModuleEvents(dict[str, list[Event]]):
    def __missing__(self, key: str) -> list[Event]:
        self[key] = list()
        return self[key]



test_example_3_2 = """
>>> event_iter = (Event.from_line(l) for l in log_data.splitlines())
>>> module_details = ModuleEvents()
>>> for event in filter(None, event_iter):
...     module_details[event.module].append(event)

>>> from pprint import pprint
>>> pprint(module_details)
{'module1': [Event(timestamp='2016-04-24 11:05:01,462', level='INFO', module='module1', message='Sample Message One'),
             Event(timestamp='2016-04-24 11:07:03,246', level='WARNING', module='module1', message='Something might have gone wrong')],
 'module2': [Event(timestamp='2016-04-24 11:06:02,624', level='DEBUG', module='module2', message='Debugging')]}
"""


# End of Using more complex structures -- maps of lists

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
