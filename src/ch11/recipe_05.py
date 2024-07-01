# Python Cookbook, 3rd Ed.
#
# Chapter: Input/Output, Physical Format, and Logical Layout
# Recipe: Reading complex formats using regular expressions



log_data = """
[2016-05-08 11:08:18,651] INFO in ch09_r09: Sample Message One
[2016-05-08 11:08:18,651] DEBUG in ch09_r09: Debugging
[2016-05-08 11:08:18,652] WARNING in ch09_r09: Something might have gone wrong
"""


# Subection: Getting ready

import re

pattern_text = (
    r"\[(?P<date>.*?)]\s+"
    r"(?P<level>\w+)\s+"
    r"in\s+(?P<module>\S+?)"
    r":\s+(?P<message>.+)"
    )

pattern = re.compile(pattern_text, re.X)

test_example_2_2 = """
>>> sample_data = '[2016-05-08 11:08:18,651] INFO in ch10_r09: Sample Message One'

>>> match = pattern.match(sample_data)
>>> match.groups()
('2016-05-08 11:08:18,651', 'INFO', 'ch10_r09', 'Sample Message One')

>>> match.groupdict()
{'date': '2016-05-08 11:08:18,651', 'level': 'INFO', 'module': 'ch10_r09', 'message': 'Sample Message One'}
"""

# Subection: How to do it...
# Topic: Defining the parse function

import re

# pattern_text = (
#     r"\[(?P<date>.*?)\]\s+"
#     r"(?P<level>\w+)\s+"
#     r"in\s+(?P<module>\S+?)"
#     r":\s+(?P<message>.+)"
#     )

pattern = re.compile(pattern_text, re.X)

from typing import NamedTuple

class LogLine(NamedTuple):
    date: str
    level: str
    module: str
    message: str

def log_parser(source_line: str) -> LogLine:
    if match := pattern.match(source_line):
        data = match.groupdict()
        return LogLine(**data)
    raise ValueError(f"Unexpected input {source_line=}")


# Subection: How to do it...
# Topic: Using the log\_parser() function

from pathlib import Path

test_log_parser = """
>>> from pathlib import Path
>>> from pprint import pprint
>>> data_path = Path("data") / "sample.log"
>>> with data_path.open() as data_file:
...     data_reader = map(log_parser, data_file)
...     for row in data_reader:
...         pprint(row)        
LogLine(date='2016-06-15 17:57:54,715', level='INFO', module='ch09_r10', message='Sample Message One')
LogLine(date='2016-06-15 17:57:54,715', level='DEBUG', module='ch09_r10', message='Debugging')
LogLine(date='2016-06-15 17:57:54,715', level='WARNING', module='ch09_r10', message='Something might have gone wrong')
"""

# Subection: How it works...

import csv

def syntax_check() -> None:
    some_path = Path("data")
    with some_path.open() as data_file:
        data_reader_csv = csv.DictReader(data_file)

        data_reader_logs = map(log_parser, data_file)

# Subection: There's more...

import csv

def copy(data_path: Path) -> None:
    target_path = data_path.with_suffix(".csv")
    with target_path.open("w", newline="") as target_file:
        writer = csv.DictWriter(target_file, LogLine._fields)
        writer.writeheader()
        with data_path.open() as data_file:
            reader = map(log_parser, data_file)
            writer.writerows(row._asdict() for row in reader)

sample_data = """
date,level,module,message
"2016-06-15 17:57:54,715",INFO,ch09_r10,Sample Message One
"2016-06-15 17:57:54,715",DEBUG,ch09_r10,Debugging
"2016-06-15 17:57:54,715",WARNING,ch09_r10,Something might have gone wrong
"""

test_copy = """
>>> from pathlib import Path
>>> source = Path("data/sample.log")
>>> copy(source)
>>> output = Path("data/sample.csv").read_text()
>>> output.splitlines() == ['date,level,module,message', '"2016-06-15 17:57:54,715",INFO,ch09_r10,Sample Message One', '"2016-06-15 17:57:54,715",DEBUG,ch09_r10,Debugging', '"2016-06-15 17:57:54,715",WARNING,ch09_r10,Something might have gone wrong']
True
"""
# End of Reading complex formats using regular expressions

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
