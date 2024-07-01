# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Using a class as a namespace for configuration


# Subection: Getting ready

test_example_1 = """
>>> from settings import Configuration
>>> Configuration.base
'https://forecast.weather.gov/shmrn.php'
"""

from pathlib import Path


ConfigClass = type[object]

def load_config_file_draft(
    config_path: Path, classname: str = "Configuration"
) -> ConfigClass:
    """Loads a configuration mapping object with contents
    of a given file.

    :param config_path: Path to be read.

    :returns: mapping with configuration parameter values
    """
    # Details omitted.
    return object

# Subection: How to do it...


from pathlib import Path
import platform

def load_config_file(
    config_path: Path, classname: str = "Configuration"
) -> ConfigClass:
    code = compile(
        config_path.read_text(),
        config_path.name,
        "exec")
    globals = {
        "__builtins__": __builtins__,
        "Path": Path,
        "platform": platform}
    locals: dict[str, ConfigClass] = {}
    exec(code, globals, locals)
    return locals[classname]

test_example_2 = """
>>> configuration = load_config_file(
... Path('src/ch13/settings.py'), 'Chesapeake')

>>> configuration.__doc__.strip()
'Weather for Chesapeake Bay'
>>> configuration.query 
{'mz': ['ANZ532']}
>>> configuration.base
'https://forecast.weather.gov/shmrn.php'
"""

# Subection: There's more...

code_example = """
% python3 some_app.py -c settings.Chesapeake
"""

import importlib

def load_config_class(name: str) -> ConfigClass:
    module_name, _, class_name = name.rpartition(".")
    settings_module = importlib.import_module(module_name)
    result: ConfigClass = vars(settings_module)[class_name]
    return result

test_example_3_4 = """
>>> configuration = load_config_class(
... 'settings.Chesapeake')

>>> configuration.__doc__.strip()
'Weather for Chesapeake Bay'
>>> configuration.query 
{'mz': ['ANZ532']}
>>> configuration.base
'https://forecast.weather.gov/shmrn.php'

"""

# Subection: There's more...
# Topic: Configuration representation


test_example_4_1 = """
>>> configuration = load_config_class(
... 'settings.Chesapeake')

>>> print(configuration)
<class 'settings.Chesapeake'>


>>> from pprint import pprint
>>> pprint(vars(configuration))
mappingproxy({'__doc__': '\\n    Weather for Chesapeake Bay\\n    ',
              '__module__': 'settings',
              'query': {'mz': ['ANZ532']}})
"""


class ConfigMetaclass(type):
    """Displays a subclass with superclass values injected"""
    def __repr__(self) -> str:
        name = (
            super().__name__
            + "("
            + ", ".join(b.__name__ for b in super().__bases__)
            + ")"
        )

        base_values = {
            n: v
            for base in reversed(super().__mro__)
                for n, v in vars(base).items()
                    if not n.startswith("_")
        }

        values_text = [f"class {name}:"] + [
            f"    {name} = {value!r}"
            for name, value in base_values.items()
        ]

        return "\n".join(values_text)


class Configuration(metaclass=ConfigMetaclass):
    unchanged = "default"
    override = "default"
    feature_x_override = "default"
    feature_x = "disabled"

class Customized(Configuration):
    override = "customized"
    feature_x_override = "x-customized"

test_example_4_5 = """
>>> print(Customized)
class Customized(Configuration):
    unchanged = 'default'
    override = 'customized'
    feature_x_override = 'x-customized'
    feature_x = 'disabled'
"""


# End of Using a class as a namespace for configuration

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
