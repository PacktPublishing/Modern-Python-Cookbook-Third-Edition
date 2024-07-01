# Python Cookbook, 3rd Ed.
#
# Chapter: Documentation and Style
# Recipe: Using Sphinx autodoc to create the API reference

"""
Tests classes that compute summary statistics from
larger data structures.

-   :py:class:`stats.StatsList`

-   Others are possible
"""

import pytest

import stats
import stats_0

@pytest.fixture(params=[stats.StatsList, stats_0.StatsList])
def instances(request):
    cls = request.param
    d_1 = cls([10, 8, 13, 9, 11])
    d_2 = cls([14, 6, 4, 12, 7, 5])
    return d_1, d_2

def test_stats_list(instances) -> None:
    subset1, data = instances

    # List-like behavior
    data.extend(subset1)
    assert data == [14, 6, 4, 12, 7, 5, 10, 8, 13, 9, 11]

    # Statistical summaries
    assert data.mean() == pytest.approx(9.0)
    assert data.variance() == pytest.approx(11.0)
