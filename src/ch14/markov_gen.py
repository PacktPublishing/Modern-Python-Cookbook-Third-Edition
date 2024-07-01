"""
Python Cookbook, 3rd Ed.

Chapter 14, Application Integration: Combination
Markov Generator
"""
import argparse
from collections.abc import Callable
from contextlib import redirect_stdout
import csv
from functools import partial
import os
from pathlib import Path
import random
import sys
from textwrap import dedent
from typing import TypeAlias, Any, TextIO

Chain: TypeAlias = list[int]
State: TypeAlias = Callable[[Chain, int], tuple[Chain, Any]]


class Succeed(Exception):
    pass


class Fail(Exception):
    pass


def start(chain: Chain, roll: int) -> tuple[Chain, State]:
    if roll in {7, 11}:
        return chain + [roll], succeed
    elif roll in {2, 3, 12}:
        return chain + [roll], fail
    else:
        return chain + [roll], partial(grow_until, roll)


def grow_until(point: int, chain: Chain, roll: int) -> tuple[Chain, State]:
    if roll in {7}:
        return chain + [roll], fail
    elif roll == point:
        return chain + [roll], succeed
    else:
        return chain + [roll], partial(grow_until, point)


def succeed(chain: Chain, roll: int) -> tuple[Chain, State]:
    raise Succeed(chain)


def fail(chain: Chain, roll: int) -> tuple[Chain, State]:
    raise Fail(chain)


class Dice:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self.roll()

    def roll(self) -> tuple[int, ...]:
        self.dice = (self._rng.randint(1, 6), self._rng.randint(1, 6))
        return self.dice


def make_chain(dice: Dice) -> tuple[str, Chain]:
    state: State = start
    chain: Chain = []
    try:
        while True:
            roll = sum(dice.roll())
            chain, state = state(chain, roll)
    except Succeed:
        return ("Success", chain)
    except Fail:
        return ("Fail", chain)


class Writer:
    def __init__(self, target: TextIO | None = None) -> None:
        self.target = target

    def header(self, opts: argparse.Namespace, columns: bool = True) -> None:
        ...

    def sample(self, outcome: str, chain: list[int]) -> None:
        ...


class CSVWriter(Writer):
    def __init__(self, target: TextIO | None = None) -> None:
        super().__init__(target)

    def header(self, opts: argparse.Namespace, columns: bool = True) -> None:
        print(f'# file = "{opts.output}"', file=self.target)
        print(f"# samples = {opts.samples}", file=self.target)
        print(f"# randomize = {opts.randomize}", file=self.target)
        if columns and self.target:
            print("# -----", file=self.target)
            self.writer = csv.writer(self.target)
            self.writer.writerow(["outcome", "length", "chain"])

    def sample(self, outcome: str, chain: list[int]) -> None:
        self.writer.writerow([outcome, len(chain), ";".join(map(str, chain))])


class TOMLWriter(Writer):
    def __init__(self, target: TextIO | None = None) -> None:
        super().__init__(target or sys.stdout)

    def header(self, opts: argparse.Namespace, columns: bool = True) -> None:
        with redirect_stdout(self.target):
            print("[Configuration]")
            print(f'  file = "{opts.output}"')
            print(f"  samples = {opts.samples}")
            print(f"  randomize = {opts.randomize}")

    def sample(self, outcome: str, chain: list[int]) -> None:
        with redirect_stdout(self.target):
            print("[[Samples]]")
            print(f'  outcome = "{outcome}"')
            print(f"  length = {len(chain)}")
            print(f"  chain = {chain}")


def write_samples(target_file: TextIO, opts: argparse.Namespace) -> None:
    if opts.randomize:
        probe_sequence = Dice(opts.randomize)
    else:
        probe_sequence = Dice()

    writer = CSVWriter(target_file)
    writer.header(opts, columns=True)
    for i in range(opts.samples):
        outcome, chain = make_chain(probe_sequence)
        writer.sample(outcome, chain)


def get_options(argv: list[str]) -> argparse.Namespace:
    try:
        default_seed = int(os.environ.get("RANDOMSEED", 0))
    except ValueError:
        default_seed = 0
    parser = argparse.ArgumentParser(description="Markov Chain Generator")
    parser.add_argument("-s", "--samples", type=int, default=100)
    parser.add_argument("-r", "--randomize", type=int, default=default_seed)
    parser.add_argument("-o", "--output", type=Path, default=None)
    options = parser.parse_args(argv)
    return options


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)

    if options.output:
        with options.output.open("w") as target_file:
            write_samples(target_file, options)
        # Summary
        writer = CSVWriter()
        writer.header(options, columns=False)
    else:
        write_samples(sys.stdout, options)


if __name__ == "__main__":
    main()
