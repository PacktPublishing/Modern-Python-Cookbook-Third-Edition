# Python Cookbook, 3rd Ed.
#
# Chapter: More Advanced Class Design
# Recipe: Managing global and singleton objects


from collections import Counter

_global_counter: Counter[str] = Counter()

def count(key: str, increment: int = 1) -> None:
    _global_counter[key] += increment

def counts() -> list[tuple[str, int]]:
    return _global_counter.most_common()
