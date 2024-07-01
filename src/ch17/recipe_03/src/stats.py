# Python Cookbook, 3rd Ed.
#
# Chapter: Documentation and Style
# Recipe: Using Sphinx autodoc to create the API reference

"""
Defines classes that compute summary statistics from
larger data structures.

-   :py:class:`StatsList`

-   Others are possible
"""

import math


class StatsList(list[float]):
    """
    A list of float (or int) values that computes some essential statistics.

    >>> x = StatsList([1, 2, 3, 4])
    >>> x.mean()
    2.5
    """

    def sum(self) -> float:
        """
        Sum of items in the list.
        """
        return sum(v for v in self)

    def size(self) -> float:
        """
        The size of the list.
        This is often the :py:func:`len` but a subclass may define a filter
        to exclude values.
        """
        return sum(1 for v in self)

    def mean(self) -> float:
        """
        The mean of values in the list.
        """
        return self.sum() / self.size()

    def sum2(self) -> float:
        """
        Sum of squares of items in the list.
        """
        return sum(v**2 for v in self)

    def variance(self) -> float:
        r"""
        Variance of items in the list.

        ..  math::

            \sigma^2 = \frac{\sum x^2 - \frac{(\sum x)^2}{N}}{N-1}
        """
        return (self.sum2() - self.sum() ** 2 / self.size()) / (self.size() - 1)

    def stddev(self) -> float:
        """
        Standard deviation of the list.
        """
        return math.sqrt(self.variance())
