# Python Cookbook, 3rd Ed.
#
# Chapter: Built-In Data Structures Part 1: Lists and Sets
# Recipe: Choosing a data structure


# Subsection: How to do it...

def confirm() -> bool:
    yes = {"yes", "y"}
    no = {"no", "n"}
    while (answer := input("Confirm: ")).lower() not in (yes | no):
        print("Please respond with yes or no")
    return answer in yes

test_example_1_2 = """
>>> yes = {"yes", "y"}
>>> no = {"no", "n"}
>>> valid_inputs = yes | no
>>> valid_inputs.add("y")
>>> valid_inputs == {'yes', 'no', 'n', 'y'}
True
"""

test_example_1_3 = """
>>> month_name_list = ["Jan", "Feb", "Mar", "Apr",
... "May", "Jun", "Jul", "Aug",
... "Sep", "Oct", "Nov", "Dec"]
>>> month_name_list[8]
'Sep'
>>> month_name_list.index("Feb")
1
"""

test_example_1_4 = """
>>> scheme = {"Crimson": (220, 14, 60),
... "DarkCyan": (0, 139, 139),
... "Yellow": (255, 255, 00)}
>>>
scheme['Crimson']
(220, 14, 60)
"""


# End of Choosing a data structure

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
