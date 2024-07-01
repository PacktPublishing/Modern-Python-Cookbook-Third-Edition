# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Testing things that involve randomness


# Subsection: Getting ready

from collections.abc import Iterator
import random

def resample(population: list[int], N: int) -> Iterator[int]:
    for i in range(N):
        sample = random.choice(population)
        yield sample



from collections import Counter
import statistics

def mean_distribution(population: list[int], N: int) -> Counter[float]:
    means: Counter[float] = Counter()
    for _ in range(1000):
        subset = list(resample(population, N))
        measure = round(statistics.mean(subset), 1)
        means[measure] += 1
    return means



test_example_1_3 = """
>>> random.seed(42)
>>> population = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]

>>> mean_distribution(population, 4).most_common(5)
[(7.8, 51), (7.2, 45), (7.5, 44), (7.1, 41), (7.7, 40)]
"""

# End of Testing things that involve randomness

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
