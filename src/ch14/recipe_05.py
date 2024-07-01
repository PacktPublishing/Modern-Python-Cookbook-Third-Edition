# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Wrapping a program and checking the output


# Subsection: Getting ready

bash_example = """
(cookbook) % RANDOMSEED=42 src/ch14/markov_gen --samples 5 --output t.csv 
# file = "t.csv"
# samples = 5
# randomize = 42

"""


# Subsection: How to do it...

import argparse
from collections.abc import Iterable, Iterator
from pathlib import Path
import subprocess
import sys
from typing import Any




def spike_1() -> None:
    directory, n = Path("/tmp"), 42
    filename = directory / f"sample_{n}.toml"
    temp_path = directory / "stdout.txt"
    command = [
        "src/ch14/markov_gen",
        "--samples", "10",
        "--output", str(filename),
    ]
    with temp_path.open("w") as temp_file:
        process = subprocess.run(
            command,
            stdout=temp_file, check=True, text=True
        )
    output_text = temp_path.read_text()


def command_output(
    temporary: Path, command: list[str]
) -> str:
    temp_path = temporary / "stdout"
    with temp_path.open("w") as temp_file:
        subprocess.run(
            command,
            stdout=temp_file, check=True, text=True
        )
    output_text = temp_path.read_text()
    temp_path.unlink()
    return output_text


import re

def parse_output(result: str) -> dict[str, Any]:
    matches = (
        re.match(r"^#\s*([^\s=]+)\s*=\s*(.*?)\s*$", line)
        for line in result.splitlines()
    )
    match_groups = (
        match.groups()
        for match in matches
        if match
    )
    summary = {
        name: value
        for name, value in match_groups
    }
    return summary





def command_iter(options: argparse.Namespace) -> Iterable[list[str]]:
    for n in range(options.iterations):
        filename = options.directory / f"sample_{n}.csv"
        command = [
            "src/ch14/markov_gen",
            "--samples", str(options.samples),
            "--output", str(filename),
            "--randomize", str(n+1),
        ]
        yield command


def get_options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("-s", "--samples", type=int, default=1_000)
    parser.add_argument("-i", "--iterations", type=int, default=10)
    options = parser.parse_args(argv)
    return options


import tempfile

def summary_iter(options: argparse.Namespace) -> Iterator[dict[str, Any]]:
    commands = command_iter(options)
    with tempfile.TemporaryDirectory() as tempdir:
        results = (
            command_output(Path(tempdir), cmd)
            for cmd in commands
        )
        for text in results:
            yield parse_output(text)


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    parsed_results = list(summary_iter(options))
    print(f"Built {len(parsed_results)} files")
    # print(parsed_results)
    total = sum(
        int(rslt['samples']) for rslt in parsed_results
    )
    print(f"Total {total} samples")


if __name__ == "__main__":
    main()


test_main = """
>>> main(["--iterations", "10", "data/ch14"])
Built 10 files
Total 10000 samples
"""

# Subsection: There's more...


import csv

def main_2(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)

    total_counter = 0
    wtr = csv.DictWriter(sys.stdout, ["file", "samples", "randomize"])
    wtr.writeheader()
    for summary in summary_iter(options):
        wtr.writerow(summary)
        total_counter += int(summary["samples"])
    wtr.writerow({"file": "TOTAL", "samples": total_counter})


test_main_2 = '''
>>> main_2(["--iterations", "10", "data/ch14"])
file,samples,randomize\r
"""data/ch14/sample_0.csv""",1000,1\r
"""data/ch14/sample_1.csv""",1000,2\r
"""data/ch14/sample_2.csv""",1000,3\r
"""data/ch14/sample_3.csv""",1000,4\r
"""data/ch14/sample_4.csv""",1000,5\r
"""data/ch14/sample_5.csv""",1000,6\r
"""data/ch14/sample_6.csv""",1000,7\r
"""data/ch14/sample_7.csv""",1000,8\r
"""data/ch14/sample_8.csv""",1000,9\r
"""data/ch14/sample_9.csv""",1000,10\r
TOTAL,10000,\r
'''

# End of Wrapping a program and checking the output

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
