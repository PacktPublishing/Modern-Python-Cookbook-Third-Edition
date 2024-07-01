# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Combining two applications into one

from collections.abc import Callable, Iterator
import contextlib
import io
from pathlib import Path
import time
from typing import Any, Literal

from recipe_01 import gen_and_summ, parallel_generators


def cleanup() -> Iterator[Literal[None]]:
    Path("data/ch14").mkdir(parents=True, exist_ok=True)
    yield None
    data = Path("data/ch14")
    for file in data.glob("*.csv"):
        file.unlink()
    data.rmdir()


def benchmark(f: Callable[..., Any], args: Any, **kwargs: Any) -> list[float]:
    timing: list[float] = []
    for sample in range(4):
        fixture_iter = iter(cleanup())
        next(fixture_iter)
        start = time.perf_counter()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            f(*args, **kwargs)
        end = time.perf_counter()
        try:
            next(fixture_iter)
        except StopIteration:
            pass
        timing.append(end - start)
    return timing


from statistics import mean
import multiprocessing


def stats(label: str, series: list[float]) -> None:
    m = mean(series)
    a = max(series)
    i = min(series)
    print(f"{label:22s} {i:7.3f} {m:6.2f} {a:7.3f} ")


def main() -> None:
    serial = benchmark(gen_and_summ, (500, 1000))
    parallel = benchmark(parallel_generators, (500, 1000))
    parallel_16 = benchmark(parallel_generators, (500, 1000), workers=16)

    workers = multiprocessing.cpu_count()
    stats("Serial", serial)
    stats(f"Parallel ({workers} workers)", parallel)
    stats("Parallel (16 workers)", parallel_16)


if __name__ == "__main__":
    main()
