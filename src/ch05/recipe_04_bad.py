# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Writing dictionary-related type hints

# Subsection: How it works...

import datetime
from typing import TypedDict

class History (TypedDict):
    date: datetime.date
    start_time: datetime.time
    start_fuel: float
    end_time: datetime.time
    end_fuel: float

result: History = {'date': 42}
