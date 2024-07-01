# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Designing scripts for composition


# Subection: Getting ready

def main() -> None:
    # The real work of this script.
    pass


# Subection: How to do it...

"""
    Some Script.
    What it does. How it works.
    Who uses it. When do they use it.
"""
if __name__ == "__main__":
    main()

# Subection: There's more...

# # Some complicated process
#
# Some additional markdown details.

# In[12]:

print("Some useful code here")

# In[21]:

print("More code here")
####################################
# Some complicated process         #
#                                  #
# Some additional markdown details.#
####################################

print("Some useful code here")

####################################
# Another step in the process      #
####################################

print("More code here")


# End of Designing scripts for composition

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
