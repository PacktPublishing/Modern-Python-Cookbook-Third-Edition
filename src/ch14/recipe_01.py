# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Combining two applications into one


TOML_example = """
[Configuration]
  file = "../../data/ch14/data.toml"
  samples = 10
  randomize = 0
[[Samples]]
  outcome="Fail"
  length=4
  chain=[6, 10, 12, 7]
[[Samples]]
  outcome="Fail"
  length=6
  chain=[6, 5, 2, 8, 5, 7]
"""

CSV_example = """
# file = "../../data/ch14/data.csv"
# samples = 10
# randomize = 0
# -----
outcome,length,chain
"Success",1,"7"
"Success",2,"10;10"
"""


# Subsection: Getting ready

# Subsection: How to do it...

import argparse
import contextlib
import logging
from pathlib import Path
import sys

import markov_gen
import markov_summ


def gen_and_summ(iterations: int, samples: int) -> None:
    for i in range(iterations):
        markov_gen.main(
            [
                "--samples", str(samples),
                "--randomize", str(i + 1),
                "--output", f"data/ch14/markov_{i}.csv",
            ]
        )
    markov_summ.main()





def get_options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Markov Chain Generator and Summary")
    parser.add_argument("-s", "--samples", type=int, default=1_000)
    parser.add_argument("-i", "--iterations", type=int, default=10)
    return parser.parse_args(argv)


def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    target = Path.cwd() / "summary.md"
    with target.open("w") as target_file:
        with contextlib.redirect_stdout(target_file):
            gen_and_summ(options.iterations, options.samples)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    main()

# Subsection: There's more...
# Topic: Structure


# Subsection: There's more...
# Topic: Performance

import io

def generator_function(samples: int, i: int) -> str:
    temp_file = io.StringIO()
    with contextlib.redirect_stdout(temp_file):
        markov_gen.main(
            [
                "--samples", str(samples),
                "--randomize", str(i + 1),
                "--output", f"data/ch14/markov_{i}.csv",
            ]
        )
    return temp_file.getvalue()



from concurrent import futures

def parallel_generators(
    iterations: int = 10, samples: int = 1_000, workers: int | None = None
) -> None:
    worker_list = []
    reports = []
    # Fan-out the generators
    with futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for i in range(iterations):
            worker_list.append(executor.submit(generator_function, samples, i))
        for worker in worker_list:
            gen_report = worker.result()
            reports.append(gen_report)

    # Fan-in and reduce
    for rpt in reports:
        print(rpt)
    markov_summ.main()


test_parallel_serial = """
# Clear out clutter from data/ch14/*.csv files.
>>> from pathlib import Path
>>> for f in Path("data/ch14").glob("*.csv"):
...     f.unlink()

# Serial
>>> Path("data/ch14").mkdir(exist_ok=True)
>>> gen_and_summ(10, 1000)
# file = "data/ch14/markov_0.csv"
# samples = 1000
# randomize = 1
...
{'Fail': 5109, 'Success': 4891}
...
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |     5109 |
+----------+----------+
| Success  |     4891 |
+==========+==========+
...

# Parallel
>>> parallel_generators(10, 1000)
# file = "data/ch14/markov_0.csv"
# samples = 1000
# randomize = 1
...
{'Fail': 5109, 'Success': 4891}
...
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |     5109 |
+----------+----------+
| Success  |     4891 |
+==========+==========+
...

"""


# Subsection: There's more...
# Topic: Logging

if __name__ == "__main__":
    # logging configuration should only go here.
    main()
    logging.shutdown()


# End of Combining two applications into one

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
