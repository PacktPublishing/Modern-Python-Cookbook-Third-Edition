# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Managing arguments and configuration in composite applications


# Subsection: How to do it...

bash_examples = """
markov generate -o detail_file.csv -s samples
markov summarize -o summary_file.md detail_file.csv ...

markov gensumm -g samples
"""

import argparse
import sys
from typing import Any


class Command:
    @classmethod
    def arguments(
            cls,
            sub_parser: argparse.ArgumentParser
    ) -> None:
        pass

    def __init__(self) -> None:
        pass

    def execute(self, options: argparse.Namespace) -> None:
        pass


import os
import markov_gen


class Generate(Command):
    @classmethod
    def arguments(
            cls,
            generate_parser: argparse.ArgumentParser
    ) -> None:
        default_seed = os.environ.get("RANDOMSEED", "0")
        generate_parser.add_argument(
            "-s", "--samples", type=int, default=1_000)
        generate_parser.add_argument(
            "-o", "--output", dest="output")
        generate_parser.add_argument(
            "-r", "--randomize", default=default_seed)
        generate_parser.set_defaults(command=cls)

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
from pathlib import Path
import markov_summ_2


class Summarize(Command):
    @classmethod
    def arguments(
            cls,
            summarize_parser: argparse.ArgumentParser
    ) -> None:
        summarize_parser.add_argument(
            "-o", "--output", dest="summary_file")
        summarize_parser.add_argument(
            "output_files", nargs="*", type=Path)
        summarize_parser.set_defaults(command=cls)

    def execute(self, options: argparse.Namespace) -> None:
        output_paths = [Path(f) for f in options.output_files]
        outcomes, lengths = markov_summ_2.process_files(output_paths)
        if options.summary_file:
            self.summary_path = Path(options.summary_file)
            with self.summary_path.open("w") as result_file:
                with contextlib.redirect_stdout(result_file):
                    markov_summ_2.write_report(outcomes, lengths)
        else:
            markov_summ_2.write_report(outcomes, lengths)


class GenSumm(Command):
    @classmethod
    def arguments(
            cls,
            gensumm_parser: argparse.ArgumentParser
    ) -> None:
        default_seed = os.environ.get("RANDOMSEED", "0")
        gensumm_parser.add_argument(
            "-s", "--samples", type=int, default=1_000)
        gensumm_parser.add_argument(
            "-o", "--output", dest="summary_file.md")
        gensumm_parser.add_argument(
            "-r", "--randomize", default=default_seed)
        gensumm_parser.set_defaults(command=cls)


import argparse

def get_options(
        argv: list[str]
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Markov")
    subparsers = parser.add_subparsers()
    generate_parser = subparsers.add_parser("generate")
    Generate.arguments(generate_parser)

    summarize_parser = subparsers.add_parser("summarize")
    Summarize.arguments(summarize_parser)
    gensumm_parser = subparsers.add_parser("gensumm")
    GenSumm.arguments(gensumm_parser)
    options = parser.parse_args(argv)
    if "command" not in options:
        parser.error("No command selected")
    return options


from typing import cast


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    command = cast(type[Command], options.command)()
    command.execute(options)


bash_examples_2 = """
python recipe_03.py $*
python -m recipe_03 $*
"""

# Subsection: How it works...

bash_examples_3 = """
markov generate -g 100 -o x.toml
Namespace(command=<class '__main__.Generate'>, output='x.toml', samples=100)
"""

# Subsection: There's more...


def get_options_2(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="markov")
    subparsers = parser.add_subparsers()
    sub_commands = [
        ("generate", Generate),
        ("summarize", Summarize),
        ("gensumm", GenSumm),
    ]

    for name, subc in sub_commands:
        cmd_parser = subparsers.add_parser(name)
        subc.arguments(cmd_parser)
    # The parsing and validating remains the same...
    options = parser.parse_args(argv)
    if "command" not in options:
        parser.error("No command selected")
    return options


def get_options_3(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="markov")
    subparsers = parser.add_subparsers()
    for subc in Command.__subclasses__():
        cmd_parser = subparsers.add_parser(subc.__name__.lower())
        subc.arguments(cmd_parser)
    options = parser.parse_args(argv)
    if "command" not in options:
        parser.error("No command selected")
    return options


if __name__ == "__main__":
    main()


import subprocess
import os


def shell(commands: str) -> None:
    env = os.environ
    env["PYTHONPATH"] = "src/ch14"
    for line in (l.rstrip() for l in commands.splitlines()):
        if not line:
            continue
        command = line.lstrip("% ")
        try:
            result = subprocess.run(
                command, shell=True, check=True, text=True, capture_output=True
            )
            print(result.args)
            if result.stderr:
                print("ERROR", result.stderr)
            for line in result.stdout.splitlines():
                print(line)
        except subprocess.CalledProcessError as ex:
            print(ex.cmd)
            print(ex)
            print(ex.stderr)


test_shell = '''
>>> shell("""
... % python src/ch14/recipe_03.py generate --samples 10 --output data/ch14_r03.csv
... % echo PYTHONPATH = $PYTHONPATH
... % python -m recipe_03 summarize data/ch14_r03.csv
... """)
python src/ch14/recipe_03.py generate --samples 10 --output data/ch14_r03.csv
Created data/ch14_r03.csv
echo PYTHONPATH = $PYTHONPATH
PYTHONPATH = src/ch14
python -m recipe_03 summarize data/ch14_r03.csv
## Overview
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |        4 |
+----------+----------+
| Success  |        6 |
+==========+==========+
...

'''

test_options_2 = """
>>> get_options_2(["generate", "-o", "file.csv", "-r", "42", "-s", "10"])
Namespace(samples=10, output='file.csv', randomize='42', command=<class 'recipe_03.Generate'>)
"""

test_options_3 = """
>>> get_options_3(["summarize", "-o", "file.csv"])
Namespace(summary_file='file.csv', output_files=[], command=<class 'recipe_03.Summarize'>)
"""

# End of Managing arguments and configuration in composite applications

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
