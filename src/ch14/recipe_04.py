# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Wrapping and combining CLI applications
import pytest

# Subsection: Getting ready

bash_examples = """
#!/usr/bin/env python
#!/usr/bin/python

chmod +x your_application_file.py

% ./your_application_file.py --samples 10 --output sample_${n}.toml
(cookbook3) % src/ch14/markov_gen -o data/ch14_r04.csv -s 100 -r 42
# file = "data/ch14_r04.csv"
# samples = 100
# randomize = 42
"""

# Subsection: How to do it...

import argparse
import subprocess
from pathlib import Path
import sys


def spike_1() -> None:
    directory, n = Path("/tmp"), 42
    filename = directory / f"sample_{n}.csv"
    command = [
        "markov_gen",
        "--samples", "10",
        "--output", str(filename),
    ]
    subprocess.run(command, check=True)


def make_files(directory: Path, files: int = 100) -> None:
    for n in range(files):
        filename = directory / f"sample_{n}.csv"
        command = [
            "markov_gen",
            "--samples", "10",
            "--output", str(filename),
        ]
        subprocess.run(command, check=True)



def get_options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("samples", type=int)
    options = parser.parse_args(argv)
    return options


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    make_files(options.directory, options.samples)


# Subsection: There's more...


def make_files_clean(directory: Path, files: int = 100) -> None:
    """Create sample data files, with cleanup after a failure."""
    try:
        make_files(directory, files)
    except subprocess.CalledProcessError as ex:
        # Remove any files.
        for partial in directory.glob("sample_*.csv"):
            partial.unlink()
        raise


# Subsection: There's more...
# Topic: Unit test

gherkin = """
Scenario: Everything Worked

Given an external application, recipe_04.py, that works correctly
When the application is invoked 3 times
Then the subprocess.run() function will be called 3 times
And the output file pattern has 3 matches.

Scenario: Something Failed

Given an external application, recipe_04.py, that works once, then fails after the first run
When the application is invoked 3 times
Then the subprocess.run() function will be called 2 times
And the output file pattern has 0 matches.
"""


from pathlib import Path
from unittest.mock import Mock, call
from pytest import fixture


@fixture
def mock_subprocess_run_good() -> Mock:
    def make_file(command: list[str], check: bool) -> None:
        for param in command:
            if param.startswith("/") and param.endswith(".csv"):
                Path(param).write_text("# mock output")

    run_function = Mock(side_effect=make_file)
    return run_function


@fixture
def mock_subprocess_run_fail() -> Mock:
    def make_file(command: list[str], check: bool) -> None:
        for param in command:
            if param.startswith("/") and param.endswith(".csv"):
                Path(param).write_text("# mock output")

    run_function = Mock(
        side_effect=[make_file, subprocess.CalledProcessError(13, ["mock", "command"])]
    )
    return run_function


def test_make_files_clean_good(
    mock_subprocess_run_good: Mock, monkeypatch: pytest.MonkeyPatch, tmpdir: Path
) -> None:
    directory = Path(tmpdir)
    with monkeypatch.context() as patch:
        patch.setattr(subprocess, "run", mock_subprocess_run_good)
        make_files_clean(directory, files=3)
    expected = [
        call(
            [
                "markov_gen",
                "--samples", "10",
                "--output", str(tmpdir / "sample_0.csv"),
            ],
            check=True,
        ),
        call(
            [
                "markov_gen",
                "--samples", "10",
                "--output", str(tmpdir / "sample_1.csv"),
            ],
            check=True,
        ),
        call(
            [
                "markov_gen",
                "--samples", "10",
                "--output", str(tmpdir / "sample_2.csv"),
            ],
            check=True,
        ),
    ]
    assert mock_subprocess_run_good.mock_calls == expected
    assert len(list(directory.glob("sample_*.csv"))) == 3


# End of Wrapping and combining CLI applications

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
