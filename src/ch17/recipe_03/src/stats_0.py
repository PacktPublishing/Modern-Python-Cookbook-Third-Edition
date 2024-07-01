# Python Cookbook, 3rd Ed.
#
# Chapter: Documentation and Style
# Recipe: Using Sphinx autodoc to create the API reference


import math


class StatsList(list[float]):
    def sum(self) -> float:
        return sum(v for v in self)

    def size(self) -> float:
        return sum(1 for v in self)

    def mean(self) -> float:
        return self.sum() / self.size()

    def sum2(self) -> float:
        return sum(v**2 for v in self)

    def variance(self) -> float:
        return (self.sum2() - self.sum() ** 2 / self.size()) / (self.size() - 1)

    def stddev(self) -> float:
        return math.sqrt(self.variance())
