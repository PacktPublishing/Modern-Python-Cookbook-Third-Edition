# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Combining pytest and doctest tests


# Subsection: Getting ready

test_example_class = '''
class Summary:
    """
    Computes summary statistics.

    >>> s = Summary()
    >>> s.add(8)
    >>> s.add(9)
    >>> s.add(9)
    >>> round(s.mean, 2)
    8.67
    >>> s.median
    9
    >>> print(str(s))
    mean = 8.67
    median = 9
    
    """
'''


import random
import pytest
from recipe_01 import Summary

@pytest.fixture()
def flat_data() -> list[int]:
    data = list(range(1001))
    random.shuffle(data)
    return data

def test_flat(flat_data: list[int]) -> None:
    summary = Summary()
    for sample in flat_data:
        summary.add(sample)
    assert summary.mean == 500
    assert summary.median == 500


# Subsection: How to do it...

output_example_1 = """
(cookbook3) % pytest recipe_07.py --doctest-modules recipe_01.py
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0
rootdir: /Users/slott/Documents/Writing/Python/Python Cookbook 3e
configfile: pytest.ini
plugins: anyio-4.0.0
collected 7 items                                                          

recipe_07.py ..                                                      [ 28%]
recipe_01.py .....                                                   [100%]

============================ 7 passed in 0.06s =============================
"""

# Subsection: There's more...

output_example_2 = """
(cookbook3) % pytest -v recipe_07.py --doctest-modules recipe_01.py
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0 -- /Users/slott/miniconda3/envs/cookbook3/bin/python
cachedir: .pytest_cache
rootdir: /Users/slott/Documents/Writing/Python/Python Cookbook 3e
configfile: pytest.ini
plugins: anyio-4.0.0
collected 7 items                                                          

recipe_07.py::recipe_07.__test__.test_example_class PASSED           [ 14%]
recipe_07.py::test_flat PASSED                                       [ 28%]
recipe_01.py::recipe_01.Summary PASSED                               [ 42%]
recipe_01.py::recipe_01.__test__.GIVEN_binom_WHEN_0_0_THEN_1 PASSED  [ 57%]
recipe_01.py::recipe_01.__test__.GIVEN_binom_WHEN_52_52_THEN_1 PASSED [ 71%]
recipe_01.py::recipe_01.binom PASSED                                 [ 85%]
recipe_01.py::recipe_01.binom2 PASSED                                [100%]

============================ 7 passed in 0.05s =============================
"""

output_example_3 = """
(cookbook3) % pytest -v recipe_06.py --doctest-modules -k 'median'
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0 -- /Users/slott/miniconda3/envs/cookbook3/bin/python
cachedir: .pytest_cache
rootdir: /Users/slott/Documents/Writing/Python/Python Cookbook 3e
configfile: pytest.ini
plugins: anyio-4.0.0
collected 3 items / 2 deselected / 1 selected                              

recipe_06.py::test_median PASSED                                     [100%]

===================== 1 passed, 2 deselected in 0.02s ======================
"""

# End of Combining pytest and doctest tests

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
