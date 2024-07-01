"""
Python Cookbook, 3rd Ed.

Chapter 14, Application Integration: Combination
Markov Summary (Version 2)
"""

# In[1]:


import argparse
from collections import Counter
import contextlib
import csv
from pathlib import Path
import sys
import tomllib
from typing import Any


def process_files(paths: list[Path]) -> tuple[Counter[str], dict[str, Counter[int]]]:
    # In[2]:

    outcome_counts: Counter[str] = Counter()
    lengths: dict[str, Counter[int]] = {
        "Fail": Counter(),
        "Success": Counter(),
    }

    # In[3]:

    for source in paths:
        with source.open() as source_file:
            line_iter = iter(source_file)
            # Skip past the header
            for line in line_iter:
                if "-----" in line:
                    break
                # print(line.rstrip())
            reader = csv.DictReader(line_iter)
            for sample in reader:
                outcome_counts[sample["outcome"]] += 1
                lengths[sample["outcome"]][int(sample["length"])] += 1

    return outcome_counts, lengths


# In[5]:


def tabulate(label: str, value: str, mapping: dict[Any, int]) -> None:
    hline2 = f"+{'='*10}+{'='*10}+"
    hline1 = f"+{'-'*10}+{'-'*10}+"

    print(hline2)
    print(f"| {label:^8s} | {value:^8s} |")
    for k, v in sorted(mapping.items()):
        print(hline1)
        print(f"| {str(k):<8s} | {v:>8d} |")
    print(hline2)


def write_report(
    outcome_counts: Counter[str], lengths: dict[str, Counter[int]]
) -> None:
    # In[6]:

    print("## Overview")
    tabulate("Outcome", "Count", outcome_counts)
    print()

    # In[7]:

    print("## Fail Chains")
    tabulate("len", "Count", lengths["Fail"])
    print()
    print("## Success Chains")
    tabulate("len", "Count", lengths["Success"])
    print()


def main(argv: list[str] = sys.argv[1:]) -> None:
    paths = list(Path("data/ch14").glob("*.csv"))
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=Path, default=None)
    parser.add_argument("data", nargs="*", type=Path, default=paths)
    options = parser.parse_args(argv)
    outcome_counts, lengths = process_files(options.data)
    if options.output:
        with options.output.open("w") as target_file:
            with contextlib.redirect_stdout(target_file):
                write_report(outcome_counts, lengths)
    else:
        write_report(outcome_counts, lengths)


if __name__ == "__main__":
    main()
