# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Finding configuration files


# Subection: Getting ready

from pathlib import Path
from typing import Any

def load_config_file(config_path: Path) -> dict[str, Any]:
    """Loads a configuration mapping object with the contents
    of a given file.
    :param config_path: Path to be read.
    :returns: mapping with configuration parameter value
    """
    # Details omitted.
    return {}


# Subection: How to do it...

from pathlib import Path
from collections import ChainMap
from typing import TextIO, Any

def get_config() -> ChainMap[str, Any]:
    system_path = Path("/etc") / "some_app" / "config"
    local_paths = [
    ".some_app_settings",
    ".some_app_config",
    ]

    configuration_items = [
        dict(
            some_setting="Default Value",
            another_setting="Another Default",
            some_option="Built-In Choice",
        )
    ]

    if system_path.exists():
        configuration_items.append(
            load_config_file(system_path))

    for config_name in local_paths:
        config_path = Path.home() / config_name
        if config_path.exists():
            configuration_items.append(
                load_config_file(config_path))
            break

    configuration = ChainMap(
        *reversed(configuration_items)
    )
    return configuration

# Subection: How it works...


test_example_3_1 = """
>>> import collections

>>> config = collections.ChainMap(
... {'another_setting': 2},
... {'some_setting': 1},
... {'some_setting': 'Default Value',
...  'another_setting':'Another Default',
...  'some_option': 'Built-In Choice'})


>>> config['another_setting']
2

>>> config['some_setting']
1

>>> config['some_option']
'Built-In Choice'
"""

# Subection: There's more...

local_names = ('.some_app_settings', '.some_app_config')
config_paths = [
    [
        base / 'some_app' / 'config'
        for base in (Path('/etc'), Path('/opt'))
    ],
    [
        Path.home() / name
        for name in local_names
    ],
    [
        Path.cwd() / name
        for name in local_names
    ],
]

DEFAULT_CONFIGURATION: dict[str, Any] = {}

def get_config_2() -> ChainMap[str, Any]:
    configuration_items = [
        DEFAULT_CONFIGURATION
    ]
    for tier_paths in config_paths:
        for alternative in tier_paths:
            if alternative.exists():
                configuration_items.append(
                    load_config_file(alternative))
                break
    configuration = ChainMap(
        *reversed(configuration_items)
    )
    return configuration


# End of Finding configuration files

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
