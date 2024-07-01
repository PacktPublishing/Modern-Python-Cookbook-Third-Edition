# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Combining many applications using the **Command** design pattern


# Subsection: How to do it...



import argparse

class Command:
    def __init__(self) -> None:
        pass

    def execute(self, options: argparse.Namespace) -> None:
        pass


from pathlib import Path
from typing import Any
import markov_gen

class Generate(Command):
    def __init__(self) -> None:
        super().__init__()
        self.seed: Any | None = None
        self.output: Path

    def execute(self, options: argparse.Namespace) -> None:
        self.output = Path(options.output)
        with self.output.open("w") as target:
            markov_gen.write_samples(target, options)
        print(f"Created {str(self.output)}")



import contextlib
import markov_summ_2

class Summarize(Command):
    def execute(self, options: argparse.Namespace) -> None:
        self.summary_path = Path(options.summary_file)
        with self.summary_path.open("w") as result_file:
            output_paths = [Path(f) for f in options.output_files]
            outcomes, lengths = markov_summ_2.process_files(output_paths)
            with contextlib.redirect_stdout(result_file):
                markov_summ_2.write_report(outcomes, lengths)


def main() -> None:
    options_1 = argparse.Namespace(samples=1000, output="data/x.csv")
    command1 = Generate()
    command1.execute(options_1)

    options_2 = argparse.Namespace(
        summary_file="data/report.md", output_files=["data/x.csv"]
    )
    command2 = Summarize()
    command2.execute(options_2)


# Subsection: There's more...


class CmdSequence(Command):
    def __init__(self, *commands: type[Command]) -> None:
        super().__init__()
        self.commands = [command() for command in commands]

    def execute(self, options: argparse.Namespace) -> None:
        for command in self.commands:
            command.execute(options)


test_example_sequence = """
>>> from argparse import Namespace
>>> options = Namespace(
...     samples=1_000,
...     randomize=42,
...     output="data/x.csv",
...     summary_file="data/y.md",
...     output_files=["data/x.csv"]
... )

>>> both_command = CmdSequence(Generate, Summarize)
>>> both_command.execute(options)
Created data/x.csv
"""


class GenSumm(CmdSequence):
    def __init__(self) -> None:
        super().__init__(Generate, Summarize)

    def execute(self, options: argparse.Namespace) -> None:
        self.intermediate = Path("data") / "ch14_r02_temporary.toml"
        new_namespace = argparse.Namespace(
            output=str(self.intermediate),
            output_files=[str(self.intermediate)],
            **vars(options),
        )
        super().execute(new_namespace)


test_example_GenSumm = """
>>> from argparse import Namespace
>>> options = Namespace(
...     samples=1_000,
...     randomize=42,
...     summary_file="data/y2.md",
... )

>>> both_command = GenSumm()
>>> both_command.execute(options)
Created data/...
>>> print(Path("data/y2.md").read_text())
## Overview
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |      518 |
+----------+----------+
| Success  |      482 |
+==========+==========+
...
"""

# End of Combining many applications using the \textbf{Command

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
