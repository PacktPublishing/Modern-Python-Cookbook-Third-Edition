# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Creating a partial function


demo_1_1 = """
>>> from functools import reduce
>>> import operator

>>> reduce(operator.mul, ..., 1)
"""

from collections.abc import Iterable
from functools import reduce
import operator

def prod(iterable: Iterable[float]) -> float:
    return reduce(operator.mul, iterable, 1)


# subsection: Getting ready

def standardize(mean: float, stdev: float, x: float) -> float:
    return (x - mean) / stdev


from dataclasses import dataclass

@dataclass
class DataPair:
    x: float
    y: float

data_1 = [
    DataPair(x=10.0, y=8.04),
    DataPair(x=8.0, y=6.95),
    DataPair(x=13.0, y=7.58),
    DataPair(x=9.0, y=8.81),
    DataPair(x=11.0, y=8.33),
    DataPair(x=14.0, y=9.96),
    DataPair(x=6.0, y=7.24),
    DataPair(x=4.0, y=4.26),
    DataPair(x=12.0, y=10.84),
    DataPair(x=7.0, y=4.82),
    DataPair(x=5.0, y=5.68),
]

test_example_2_4 = """
>>> import statistics
>>> mean_x = statistics.mean(item.x for item in data_1)
>>> stdev_x = statistics.stdev(item.x for item in data_1)
>>> for DataPair in data_1:
...     z_x = standardize(mean_x, stdev_x, DataPair.x)
...     print(DataPair, z_x)
DataPair(x=10.0, y=8.04) 0.30151134457776363
DataPair(x=8.0, y=6.95) -0.30151134457776363
DataPair(x=13.0, y=7.58) 1.2060453783110545
DataPair(x=9.0, y=8.81) 0.0
DataPair(x=11.0, y=8.33) 0.6030226891555273
DataPair(x=14.0, y=9.96) 1.507556722888818
DataPair(x=6.0, y=7.24) -0.9045340337332909
DataPair(x=4.0, y=4.26) -1.507556722888818
DataPair(x=12.0, y=10.84) 0.9045340337332909
DataPair(x=7.0, y=4.82) -0.6030226891555273
DataPair(x=5.0, y=5.68) -1.2060453783110545
"""

# subsection: How to do it...
# Topic: Using functools.partial()

from functools import partial

test_example_3_1 = """
>>> import statistics
>>> mean_x = statistics.mean(item.x for item in data_1)
>>> stdev_x = statistics.stdev(item.x for item in data_1)

>>> z = partial(standardize, mean_x, stdev_x)

>>> for DataPair in data_1:
...     print(DataPair, z(DataPair.x))
DataPair(x=10.0, y=8.04) 0.30151134457776363
DataPair(x=8.0, y=6.95) -0.30151134457776363
DataPair(x=13.0, y=7.58) 1.2060453783110545
DataPair(x=9.0, y=8.81) 0.0
DataPair(x=11.0, y=8.33) 0.6030226891555273
DataPair(x=14.0, y=9.96) 1.507556722888818
DataPair(x=6.0, y=7.24) -0.9045340337332909
DataPair(x=4.0, y=4.26) -1.507556722888818
DataPair(x=12.0, y=10.84) 0.9045340337332909
DataPair(x=7.0, y=4.82) -0.6030226891555273
DataPair(x=5.0, y=5.68) -1.2060453783110545

"""

# subsection: How to do it...
# Topic: Creating a lambda object

test_example_3_2 = """
>>> import statistics
>>> mean_x = statistics.mean(item.x for item in data_1)
>>> stdev_x = statistics.stdev(item.x for item in data_1)

>>> z = lambda x: standardize(mean_x, stdev_x, x)

>>> for DataPair in data_1:
...     print(DataPair, z(DataPair.x))
DataPair(x=10.0, y=8.04) 0.30151134457776363
DataPair(x=8.0, y=6.95) -0.30151134457776363
DataPair(x=13.0, y=7.58) 1.2060453783110545
DataPair(x=9.0, y=8.81) 0.0
DataPair(x=11.0, y=8.33) 0.6030226891555273
DataPair(x=14.0, y=9.96) 1.507556722888818
DataPair(x=6.0, y=7.24) -0.9045340337332909
DataPair(x=4.0, y=4.26) -1.507556722888818
DataPair(x=12.0, y=10.84) 0.9045340337332909
DataPair(x=7.0, y=4.82) -0.6030226891555273
DataPair(x=5.0, y=5.68) -1.2060453783110545

"""


# subsection: How it works...

test_example_5_1 = """
>>> import statistics
>>> mean_x = statistics.mean(item.x for item in data_1)
>>> stdev_x = statistics.stdev(item.x for item in data_1)

>>> z = lambda x, m=mean_x, s=stdev_x: standardize(m, s, x)
>>> for DataPair in data_1:
...     print(DataPair, z(DataPair.x))
DataPair(x=10.0, y=8.04) 0.30151134457776363
DataPair(x=8.0, y=6.95) -0.30151134457776363
DataPair(x=13.0, y=7.58) 1.2060453783110545
DataPair(x=9.0, y=8.81) 0.0
DataPair(x=11.0, y=8.33) 0.6030226891555273
DataPair(x=14.0, y=9.96) 1.507556722888818
DataPair(x=6.0, y=7.24) -0.9045340337332909
DataPair(x=4.0, y=4.26) -1.507556722888818
DataPair(x=12.0, y=10.84) 0.9045340337332909
DataPair(x=7.0, y=4.82) -0.6030226891555273
DataPair(x=5.0, y=5.68) -1.2060453783110545
"""

# subsection: There's more...

test_example_6_2 = """
>>> prod = partial(reduce(operator.mul, initializer=1))
Traceback (most recent call last):
...
TypeError: reduce() takes no keyword arguments

"""

test_example_6_3 = """
>>> from operator import mul
>>> from functools import reduce
>>> prod = lambda x: reduce(mul, x, 1)
>>> prod(range(1,6))
120
"""

from collections.abc import Sequence, Callable
import statistics

def prepare_z(data: Sequence[DataPair]) -> Callable[[float], float]:
    mean_x = statistics.mean(item.x for item in data_1)
    stdev_x = statistics.stdev(item.x for item in data_1)
    return partial(standardize, mean_x, stdev_x)

test_example_6_5 = """
>>> z = prepare_z(data_1)
>>> for DataPair in data_1:
...     print(DataPair, z(DataPair.x))
DataPair(x=10.0, y=8.04) 0.30151134457776363
DataPair(x=8.0, y=6.95) -0.30151134457776363
DataPair(x=13.0, y=7.58) 1.2060453783110545
DataPair(x=9.0, y=8.81) 0.0
DataPair(x=11.0, y=8.33) 0.6030226891555273
DataPair(x=14.0, y=9.96) 1.507556722888818
DataPair(x=6.0, y=7.24) -0.9045340337332909
DataPair(x=4.0, y=4.26) -1.507556722888818
DataPair(x=12.0, y=10.84) 0.9045340337332909
DataPair(x=7.0, y=4.82) -0.6030226891555273
DataPair(x=5.0, y=5.68) -1.2060453783110545
"""


# End of Creating a partial function

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
