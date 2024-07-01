# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Configuration
# Recipe: Using logging for control and audit output


# Subection: How to do it...
# Topic: Logging in a class

import logging

class SomeClass:
    def __init__(self) -> None:
        self.err_logger = logging.getLogger(
            f"error.{self.__class__.__name__}")
        self.dbg_logger = logging.getLogger(
            f"debug.{self.__class__.__name__}")

    def some_method(self) -> None:
        some_variable = "some value"
        result = f"derived from {some_variable}"

        self.dbg_logger.info(
            "Some computation with %r", some_variable)
        # Some complicated computation with some_variable
        self.dbg_logger.info(
            "Result details = %r", result)
        # Some complicated input processing and parsing
        self.err_logger.info("Input processing completed.")

# Subection: How to do it...
# Topic: Logging in a function

import logging
from typing import Any

def large_and_complicated(some_parameter: Any) -> Any:
    dbg_logger = logging.getLogger("debug.large_and_complicated")
    dbg_logger.info("some_parameter= %r", some_parameter)


very_small_dbg_logger = logging.getLogger("debug.very_small")

def very_small(some_parameter: Any) -> Any:
    very_small_dbg_logger.info("some_parameter= %r", some_parameter)

# Subection: How it works...

logger = logging.getLogger(__name__)

# Subection: There's more...



from textwrap import dedent

config_toml = dedent("""
version = 1
[formatters.default]
    style = "{"
    format = "{levelname}:{name}:{message}"

[formatters.timestamp]
    style = "{"
    format = "{asctime}//{levelname}//{name}//{message}"

[handlers.console]
    class = "logging.StreamHandler"
    stream = "ext://sys.stderr"
    formatter = "default"

[handlers.file]
    class = "logging.FileHandler"
    filename = "data/write.log"
    formatter = "timestamp"

[loggers]
    overview_stats.detail = {handlers = ["console"]}
    overview_stats.write = {handlers = ["file", "console"] }
    root = {level = "INFO"}
""")

def main() -> None:
    detail_logger = logging.getLogger("overview_stats.detail")
    write_logger = logging.getLogger("overview_stats.write")
    detail_logger.info("Some details.")
    detail_logger.info("Writing the file. Count = 0")


import tomllib
import logging.config

if __name__ == "__main__":
    logging.config.dictConfig(
        tomllib.loads(config_toml))
    main()
    logging.shutdown()


# End of Using logging for control and audit output

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
