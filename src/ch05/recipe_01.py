# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Creating dictionaries -- inserting and updating


# Subsection: Getting ready

raw_data = """
[2019/11/12:08:09:10,123] INFO #PJQXB^{}eRwnEGG?2%32U path="/openapi.yaml" method=GET
[2019/11/12:08:09:10,234] INFO 9DiC!B^{}nXxnEGG?2%32U path="/items?limit=x" method=GET
[2019/11/12:08:09:10,235] INFO 9DiC!B^{}nXxnEGG?2%32U error="invalid query"
[2019/11/12:08:09:10,345] INFO #PJQXB^{}eRwnEGG?2%32U status="200" bytes="11234"
[2019/11/12:08:09:10,456] INFO 9DiC!B^{}nXxnEGG?2%32U status="404" bytes="987"
[2019/11/12:08:09:10,567] INFO >~UL>~PB_R>&nEGG?2%32U path="/category/42" method=GET
"""

import re
log_parser = re.compile(r"\[(.*?)\] (\w+) (\S+) (.*)")

matches = (
    log_parser.match(line)
    for line in raw_data.splitlines()
)
log_lines = [
    match.groups()
    for match in matches
    if match
]

test_parser = """
>>> from pprint import pprint
>>> pprint(log_lines)
[('2019/11/12:08:09:10,123',
  'INFO',
  '#PJQXB^{}eRwnEGG?2%32U',
  'path="/openapi.yaml" method=GET'),
 ('2019/11/12:08:09:10,234',
  'INFO',
  '9DiC!B^{}nXxnEGG?2%32U',
  'path="/items?limit=x" method=GET'),
 ('2019/11/12:08:09:10,235',
  'INFO',
  '9DiC!B^{}nXxnEGG?2%32U',
  'error="invalid query"'),
 ('2019/11/12:08:09:10,345',
  'INFO',
  '#PJQXB^{}eRwnEGG?2%32U',
  'status="200" bytes="11234"'),
 ('2019/11/12:08:09:10,456',
  'INFO',
  '9DiC!B^{}nXxnEGG?2%32U',
  'status="404" bytes="987"'),
 ('2019/11/12:08:09:10,567',
  'INFO',
  '>~UL>~PB_R>&nEGG?2%32U',
  'path="/category/42" method=GET')]
"""

# Subsection: How to do it...
# Topic: Building a dictionary by setting items

test_example_2_1 = """
>>> histogram = {}

>>> for line in log_lines:
...     path_method = line[3]  # group(4) of the original match
...     if path_method.startswith("path"):
...         if path_method not in histogram:
...             histogram[path_method] = 0
...         histogram[path_method] += 1

>>> histogram
{'path="/openapi.yaml" method=GET': 1, 'path="/items?limit=x" method=GET': 1, 'path="/category/42" method=GET': 1}
"""

# Subsection: How to do it...
# Topic: Building a dictionary as a comprehension

param_parser = re.compile(
    r'(\w+)=(".*?"|\w+)'
)


test_example_3_2 = """
>>> for line in log_lines:
...     name_value_pairs = param_parser.findall(line[3])
...     params = {match[0]: match[1] for match in name_value_pairs}
...     print(params)
{'path': '"/openapi.yaml"', 'method': 'GET'}
{'path': '"/items?limit=x"', 'method': 'GET'}
{'error': '"invalid query"'}
{'status': '"200"', 'bytes': '"11234"'}
{'status': '"404"', 'bytes': '"987"'}
{'path': '"/category/42"', 'method': 'GET'}

"""

# Subsection: How it works...

snippet_4_1 = """
histogram[customer] += 1
histogram[customer] = histogram[customer] + 1
"""


# Subsection: There's more...

test_example_5_1 = """
>>> histogram = {}
>>> for line in log_lines:
...     path_method = line[3]  # group(4) of the match
...     if path_method.startswith("path"):
...         _ = histogram.setdefault(path_method, 0)
...         histogram[path_method] += 1
>>> histogram
{'path="/openapi.yaml" method=GET': 1, 'path="/items?limit=x" method=GET': 1, 'path="/category/42" method=GET': 1}
"""


test_example_5_2 = """
>>> from collections import defaultdict

>>> histogram = defaultdict(int)
>>> for line in log_lines:
...     path_method = line[3]  # group(4) of the match
...     if path_method.startswith("path"):
...         histogram[path_method] += 1
>>> histogram
defaultdict(<class 'int'>, {'path="/openapi.yaml" method=GET': 1, 'path="/items?limit=x" method=GET': 1, 'path="/category/42" method=GET': 1})
"""


test_example_5_3 = """
>>> from collections import Counter

>>> histogram = Counter(
...     line[3]
...     for line in log_lines
...     if line[3].startswith("path")
... )
>>> histogram
Counter({'path="/openapi.yaml" method=GET': 1, 'path="/items?limit=x" method=GET': 1, 'path="/category/42" method=GET': 1})
"""

test_example_5_4 = """
>>> from collections import Counter

>>> filtered_paths = (
...     line[3]
...     for line in log_lines
...     if line[3].startswith("path")
... )
>>> histogram = Counter(filtered_paths)
>>> histogram
Counter({'path="/openapi.yaml" method=GET': 1, 'path="/items?limit=x" method=GET': 1, 'path="/category/42" method=GET': 1})
"""


# End of Creating dictionaries -- inserting and updating

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
