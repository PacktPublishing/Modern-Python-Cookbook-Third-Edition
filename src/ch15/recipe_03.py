# Python Cookbook, 3rd Ed.
#
# Chapter: Testing
# Recipe: Handling common doctest issues


# Subsection: Getting ready

from string import ascii_letters

def unique_letters(text: str) -> set[str]:
    letters = set(text.lower())
    non_letters = letters - set(ascii_letters)
    return letters - non_letters


class Point:
    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    @property
    def text(self) -> str:
        ns_hemisphere = "S" if self.lat < 0 else "N"
        ew_hemisphere = "W" if self.lon < 0 else "E"
        lat_deg, lat_ms = divmod(abs(self.lat), 1.0)
        lon_deg, lon_ms = divmod(abs(self.lon), 1.0)
        return (
            f"{lat_deg:02.0f}°{lat_ms*60:4.3f}′{ns_hemisphere}"
            f" {lon_deg:03.0f}°{lon_ms*60:4.3f}′{ew_hemisphere}"
        )


from math import sqrt, pi, exp, erf

def phi(n: float) -> float:
    return (1 + erf(n / sqrt(2))) / 2

def frequency(n: float) -> float:
    return phi(n) - phi(-n)




# Subsection: How to do it...
# Topic: Writing doctest examples with unpredictable set ordering

weak_test_letters = """
>>> phrase = "The quick brown fox..." 
>>> unique_letters(phrase)
{'b', 'c', 'e', 'f', 'h', 'i', 'k', 'n', 'o', 'q', 'r', 't', 'u', 'w', 'x'}
"""

test_letters_good = """
>>> phrase = "The quick brown fox..." 
>>> sorted(unique_letters(phrase))
['b', 'c', 'e', 'f', 'h', 'i', 'k', 'n', 'o', 'q', 'r', 't', 'u', 'w', 'x']
>>> (unique_letters(phrase) == 
...    {'b', 'c', 'e', 'f', 'h', 'i', 'k', 'n', 'o', 'q', 'r', 't', 'u', 'w', 'x'}
... )
True
"""


# Subsection: How to do it...
# Topic: Writing doctest examples with object IDs


test_example_3_1 = """
>>> Point(36.8439, -76.2936).text
'36°50.634′N 076°17.616′W'
"""

bad_example_3_2 = """
>>> Point(36.8439, -76.2936)
<recipe_03.Point object at 0x107910610>
"""

test_example_3_3 = """
>>> Point(36.8439, -76.2936) # doctest: +ELLIPSIS
<recipe_03.Point object at ...>
"""

test_example_3_4 = """
>>> Point(36.8439, -76.2936) #doctest: +ELLIPSIS
<...Point object at ...>
"""

# Subsection: How to do it...
# Topic: Writing doctest examples for floating-point values


test_example_4_1 = """
>>> round(phi(0), 3)
0.5
>>> round(phi(-1), 3)
0.159
>>> round(phi(+1), 3)
0.841
"""

test_example_4_2 = """
>>> from math import isclose
>>> isclose(phi(0), 0.5)
True
>>> isclose(phi(1), 0.8413, rel_tol=.0001)
True
>>> isclose(phi(2), 0.9772, rel_tol=1e-4)
True
"""

# Subsection: There's more...


# End of Handling common doctest issues

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
