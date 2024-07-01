# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Creating a class that has orderable objects

from recipe_06 import make_pinochle_card

def invalid() -> None:
    """
    >>> invalid()
    Traceback (most recent call last):
    ...
    AttributeError: 'int' object has no attribute 'rank'

    """
    c1 = make_pinochle_card(9, '♡')
    assert c1 <= 10

