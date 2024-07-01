# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Removing from dictionaries -- the pop() method and the del statement


# Subsection: Getting ready

log = """
[2019/11/12:08:09:10,123] INFO #PJQXB^{}eRwnEGG?2%32U path="/openapi.yaml" method=GET
[2019/11/12:08:09:10,234] INFO 9DiC!B^{}nXxnEGG?2%32U path="/items?limit=x" method=GET
[2019/11/12:08:09:10,235] INFO 9DiC!B^{}nXxnEGG?2%32U error="invalid query"
[2019/11/12:08:09:10,345] INFO #PJQXB^{}eRwnEGG?2%32U status="200" bytes="11234"
[2019/11/12:08:09:10,456] INFO 9DiC!B^{}nXxnEGG?2%32U status="404" bytes="987"
[2019/11/12:08:09:10,567] INFO >~UL>~PB_R>&nEGG?2%32U path="/category/42" method=GET
"""

import re
log_parser = re.compile(r"\[(.*?)\] (\w+) (\S+) (.*)")

# Subsection: How to do it...

from collections import defaultdict
from collections.abc import Iterable, Iterator

LogRec = tuple[str, ...]

def request_iter_t(source: Iterable[str]) -> Iterator[list[LogRec]]:
    requests: defaultdict[str, list[LogRec]] = defaultdict(list)

    for line in source:
        if match := log_parser.match(line):
            id = match.group(3)
            requests[id].append(tuple(match.groups()))
            if match.group(4).startswith('status'):
                yield requests[id]
                del requests[id]
    if requests:
        print("Dangling", requests)


test_request_iter_t = """
>>> from pprint import pprint
>>> log_lines = list(request_iter_t(log.splitlines()))
Dangling defaultdict(<class 'list'>, {'>~UL>~PB_R>&nEGG?2%32U': [('2019/11/12:08:09:10,567', 'INFO', '>~UL>~PB_R>&nEGG?2%32U', 'path="/category/42" method=GET')]})
>>> pprint(log_lines)
[[('2019/11/12:08:09:10,123',
   'INFO',
   '#PJQXB^{}eRwnEGG?2%32U',
   'path="/openapi.yaml" method=GET'),
  ('2019/11/12:08:09:10,345',
   'INFO',
   '#PJQXB^{}eRwnEGG?2%32U',
   'status="200" bytes="11234"')],
 [('2019/11/12:08:09:10,234',
   'INFO',
   '9DiC!B^{}nXxnEGG?2%32U',
   'path="/items?limit=x" method=GET'),
  ('2019/11/12:08:09:10,235',
   'INFO',
   '9DiC!B^{}nXxnEGG?2%32U',
   'error="invalid query"'),
  ('2019/11/12:08:09:10,456',
   'INFO',
   '9DiC!B^{}nXxnEGG?2%32U',
   'status="404" bytes="987"')]]
"""



# Subsection: There's more...

log_parser_d = re.compile(
    r"\[(?P<time>.*?)\] "
    r"(?P<sev>\w+) "
    r"(?P<id>\S+) "
    r"(?P<msg>.*)"
)

LogRecD = dict[str, str]

def request_iter_d(source: Iterable[str]) -> Iterator[list[LogRecD]]:

    requests: defaultdict[str, list[LogRecD]] = defaultdict(list)

    for line in source:
        if match := log_parser_d.match(line):
            record = match.groupdict()
            id = record.pop('id')
            requests[id].append(record)
            if record['msg'].startswith('status'):
                yield requests[id]
                del requests[id]
    if requests:
        print("Dangling", requests)


test_example_3_3 = """
>>> from pprint import pprint

>>> for r in  request_iter_d(log.splitlines()):
...     pprint(r)
[{'msg': 'path="/openapi.yaml" method=GET',
  'sev': 'INFO',
  'time': '2019/11/12:08:09:10,123'},
 {'msg': 'status="200" bytes="11234"',
  'sev': 'INFO',
  'time': '2019/11/12:08:09:10,345'}]
[{'msg': 'path="/items?limit=x" method=GET',
  'sev': 'INFO',
  'time': '2019/11/12:08:09:10,234'},
 {'msg': 'error="invalid query"',
  'sev': 'INFO',
  'time': '2019/11/12:08:09:10,235'},
 {'msg': 'status="404" bytes="987"',
  'sev': 'INFO',
  'time': '2019/11/12:08:09:10,456'}]
Dangling defaultdict(<class 'list'>, {'>~UL>~PB_R>&nEGG?2%32U': [{'time': '2019/11/12:08:09:10,567', 'sev': 'INFO', 'msg': 'path="/category/42" method=GET'}]})
"""


# End of Removing from dictionaries -- the pop() method and the del statement

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
