# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 2: Dictionaries
# Recipe: Understanding variables, references, and assignment


# Subsection: Getting ready

test_example_1_1 = """
>>> mutable = [1, 1, 2, 3, 5, 8]
>>> immutable = (5, 8, 13, 21)
"""

# Subsection: How to do it...

test_example_2_1 = """
>>> mutable = [1, 1, 2, 3, 5, 8]
>>> immutable = (5, 8, 13, 21)


>>> mutable_b = mutable
>>> immutable_b = immutable


>>> mutable_b is mutable
True
>>> immutable_b is immutable
True


>>> mutable += [mutable[-2] + mutable[-1]]


>>> immutable += (immutable[-2] + immutable[-1],)


>>> mutable_b
[1, 1, 2, 3, 5, 8, 13]
>>> mutable is mutable_b
True


>>> immutable_b
(5, 8, 13, 21)
>>> immutable
(5, 8, 13, 21, 34)
"""

# Subsection: How it works...

snippet_3_1 = """
immutable += (immutable[-2] + immutable[-1],)
immutable = immutable + (immutable[-2] + immutable[-1],)
"""

# Subsection: There's more...

snippet_4_1 = """
a = 355
a += 113
"""


# End of Understanding variables, references, and assignment

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
