# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Using a class as a namespace for configuration



class Configuration:
    """
    Generic Configuration with a sample query.
    """
    base = "https://forecast.weather.gov/shmrn.php"
    query = {"mz": ["GMZ856"]}


class Bahamas(Configuration):
    """
    Weather forecast for Offshore including the Bahamas
    """
    query = {"mz": ["AMZ117", "AMZ080"]}


class Chesapeake(Configuration):
    """
    Weather for Chesapeake Bay
    """
    query = {"mz": ["ANZ532"]}
