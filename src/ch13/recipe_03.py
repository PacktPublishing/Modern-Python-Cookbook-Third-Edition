# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Using Python for configuration files


# Subection: Getting ready

"""Weather forecast for Offshore including the Bahamas
"""

query = {'mz':
    ['ANZ532',
     'AMZ117',
     'AMZ080']
}

base_url = "https://forecast.weather.gov/shmrn.php"




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

def load_config_file(config_path: Path) -> dict[str, Any]:
    code = compile(
        config_path.read_text(),
        config_path.name,
        "exec")
    locals: dict[str, Any] = {}
    exec(
        code,
        {"__builtins__": __builtins__},
        locals
    )
    return locals

# Subection: There's more...

import os

"""Config with related paths"""
base = Path(os.environ.get("APP_HOME", "/opt/app"))
log = base / 'log'
out = base / 'out'


from pathlib import Path
import platform
import os
from typing import cast

def load_config_file_xtra(config_path: Path) -> dict[str, Any]:

    def not_allowed(*arg: Any, **kw: Any) -> None:
        raise RuntimeError("Operation not allowed")

    code = compile(
        config_path.read_text(),
        config_path.name,
        "exec")

    safe_builtins = cast(dict[str, Any], __builtins__).copy()
    for name in ("eval", "exec", "compile", "__import__"):
        safe_builtins[name] = not_allowed

    globals = {
        "__builtins__": __builtins__,
        "Path": Path,
        "platform": platform,
        "environ": os.environ.copy()
    }

    locals: dict[str, Any] = {}
    exec(code, globals, locals)
    return locals

test_load_file = """
>>> from pathlib import Path
>>> config = Path.cwd() / "data" / "config.py"
>>> _ = config.write_text('''
... base_url = "https://forecast.weather.gov/shmrn.php"
... query = {'mz': ['ANZ532']}
... ''')
>>> load_config_file(config)
{'base_url': 'https://forecast.weather.gov/shmrn.php', 'query': {'mz': ['ANZ532']}}
>>> load_config_file_xtra(config)
{'base_url': 'https://forecast.weather.gov/shmrn.php', 'query': {'mz': ['ANZ532']}}
>>> config.unlink()
"""

# End of Using Python for configuration files

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
