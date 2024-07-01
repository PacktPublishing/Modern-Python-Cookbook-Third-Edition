# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Using TOML for configuration files


example_toml = """
[some_app]
    option_1 = "useful value"
    option_2 = 42

[some_app.feature]
    option_1 = 7331
"""

test_toml_example = """
>>> from pprint import pprint
>>> import tomllib
>>> d = tomllib.loads(example_toml)
>>> pprint(d)
{'some_app': {'feature': {'option_1': 7331},
              'option_1': 'useful value',
              'option_2': 42}}
"""


# Subection: Getting ready

from pathlib import Path
from typing import Any

def load_config_file_draft(config_path: Path) -> dict[str, Any]:
    """Loads a configuration mapping object with contents
    of a given file.

    :param config_path: Path to be read.

    :returns: mapping with configuration parameter values
    """
    # Details omitted.
    return {}

# Subection: How to do it...

from pathlib import Path
from typing import Any
import tomllib

def load_config_file(config_path: Path) -> dict[str, Any]:
    """Loads a configuration mapping object with contents
    of a given file.
    :param config_path: Path to be read.
    :returns: mapping with configuration parameter values
    """
    with config_path.open('b') as config_file:
        document = tomllib.load(config_file)
    return document
    document = tomllib.loads(config_path.read_text())

# Subection: How it works...

example_2a_toml = """
some_app.option_1 = "useful value"
some_app.option_2 = 42
some_app.feature.option_1 = 7331
"""

example_2b_toml = """
[some_app]
    option_1 = "useful value"
    option_2 = 42

[some_app.feature]
    option_1 = 7331
"""

test_toml_example_2 = """
>>> from pprint import pprint
>>> import tomllib
>>> a = tomllib.loads(example_2a_toml)
>>> pprint(a)
{'some_app': {'feature': {'option_1': 7331},
              'option_1': 'useful value',
              'option_2': 42}}
>>> b = tomllib.loads(example_2b_toml)
>>> pprint(b)
{'some_app': {'feature': {'option_1': 7331},
              'option_1': 'useful value',
              'option_2': 42}}
>>> a == b
True
"""

# Subection: There's more...

example_3_toml = """
[project]
name = "python_cookbook_3e"
version = "2024.1.0"
description = "All of the code examples for Modern Python Cookbook, 3rd Ed."
readme = "README.rst"
requires-python = ">=3.12"
license = {file = "LICENSE.txt"}

[build-system]
build-backend = 'setuptools.build_meta'
requires = [
    'setuptools',
]
"""

test_toml_example_3 = """
>>> from pprint import pprint
>>> import tomllib
>>> d = tomllib.loads(example_3_toml)
>>> pprint(d)
{'build-system': {'build-backend': 'setuptools.build_meta',
                  'requires': ['setuptools']},
 'project': {'description': 'All of the code examples for Modern Python '
                            'Cookbook, 3rd Ed.',
             'license': {'file': 'LICENSE.txt'},
             'name': 'python_cookbook_3e',
             'readme': 'README.rst',
             'requires-python': '>=3.12',
             'version': '2024.1.0'}}
"""

# End of Using TOML for configuration files

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
