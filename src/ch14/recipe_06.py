# Python Cookbook, 3rd Ed.
#
# Chapter: Application Integration: Combination
# Recipe: Controlling complex sequences of steps


# Subsection: How to do it...

import argparse
import subprocess


class Command:
    def execute(self, options: argparse.Namespace) -> list[str]:
        self.command = self.os_command(options)
        results = subprocess.run(
            self.command,
            check=True, stdout=subprocess.PIPE, text=True
        )
        self.output = results.stdout
        return [self.output]

    def os_command(self, options: argparse.Namespace) -> list[str]:
        return ["echo", self.__class__.__name__, repr(options)]


import os

class Generate(Command):
    def execute(self, options: argparse.Namespace) -> list[str]:
        if "randomize" in options:
            os.environ["RANDOMSEED"] = str(options.randomize)
        return super().execute(options)

    def os_command(self, options: argparse.Namespace) -> list[str]:
        return [
            "src/ch14/markov_gen",
            "--samples", str(options.samples),
            "--output", options.output_file,
        ]


from typing import cast


class Summarize(Command):
    def os_command(self, options: argparse.Namespace) -> list[str]:
        command = [
            "python", "src/ch14/markov_summ_2.py",
        ]
        if options.summary_file:
            command += [
                "-o", str(options.summary_file),
            ]
        command += cast(list[str], options.output_files)
        return command


def demo() -> None:
    options = argparse.Namespace(
        samples=1000,
        output_file="data/x12.csv",
        output_files=["data/x12.csv"],
        summary_file=None,
        seed=42,
    )
    step1 = Generate()
    step2 = Summarize()
    output1 = step1.execute(options)
    print(step1.os_command(options))
    print(output1[0])
    output2 = step2.execute(options)
    print(step2.os_command(options))
    print(output2[0])


test_demo = """
>>> demo()
['src/ch14/markov_gen', '--samples', '1000', '--output', 'data/x12.csv']
# file = "data/x12.csv"
# samples = 1000
# randomize = 42
<BLANKLINE>
['python', 'src/ch14/markov_summ_2.py', 'data/x12.csv']
## Overview
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |      511 |
+----------+----------+
| Success  |      489 |
+==========+==========+
<BLANKLINE>
## Fail Chains
+==========+==========+
|   len    |  Count   |
+----------+----------+
| 1        |      104 |
+----------+----------+
...
+----------+----------+
| 34       |        1 |
+==========+==========+
<BLANKLINE>
## Success Chains
+==========+==========+
|   len    |  Count   |
+----------+----------+
| 1        |      210 |
+----------+----------+
...
+----------+----------+
| 24       |        1 |
+==========+==========+
<BLANKLINE>
<BLANKLINE>
"""


# Subsection: There's more...

from pathlib import Path

class IterativeGenerator(Command):

    def execute(self, options: argparse.Namespace) -> list[str]:
        gen_step = Generate()
        output_files = []
        results: list[str] = []
        for i in range(options.iterations):
            options.output_file = f"data/output_{i}.csv"
            options.randomize = i + 1
            step1_output = gen_step.execute(options)
            # Future: parse step1_output and save the summary
            results.extend(step1_output)
            output_files.append(options.output_file)
        summ_step = Summarize()
        options.output_files = output_files
        step2_output = summ_step.execute(options)
        results.extend(step2_output)
        return results

test_iteration = """
>>> options = argparse.Namespace(
...     samples=1000,
...     iterations=10,
...     summary_file=None,
... )
>>> ig = IterativeGenerator()
>>> results = ig.execute(options)
>>> len(results)
11
>>> results[0]
'# file = "data/output_0.csv"\\n# samples = 1000\\n# randomize = 1\\n'
>>> results[9]
'# file = "data/output_9.csv"\\n# samples = 1000\\n# randomize = 10\\n'
>>> print(results[10])
## Overview
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |     5108 |
+----------+----------+
| Success  |     4892 |
+==========+==========+
...
"""

# Subsection: There's more...
# Topic: Building conditional processing


class ConditionalGenSumm(Command):
    """Generator with conditional Summarization"""

    def execute(self, options: argparse.Namespace) -> list[str]:
        step1 = Generate()
        output = step1.execute(options)
        if "summary_file" in options:
            step2 = Summarize()
            output.extend(step2.execute(options))
        return output

test_conditional = """
>>> options = argparse.Namespace(
...     output_file=Path("data/x12.csv"),
...     output_files=[Path("data/x12.csv")],
...     samples=1000,
...     randomize=42,
... )
>>> cgs = ConditionalGenSumm()
>>> results = cgs.execute(options)
>>> len(results)
1
>>> results[0]
'# file = "data/x12.csv"\\n# samples = 1000\\n# randomize = 42\\n'

>>> options = argparse.Namespace(
...     output_file=Path("data/x12.csv"),
...     output_files=[Path("data/x12.csv")],
...     samples=1000,
...     randomize=42,
...     summary_file=None,
... )
>>> cgs = ConditionalGenSumm()
>>> results = cgs.execute(options)
>>> len(results)
2
>>> results[0]
'# file = "data/x12.csv"\\n# samples = 1000\\n# randomize = 42\\n'
>>> print(results[1])
## Overview
+==========+==========+
| Outcome  |  Count   |
+----------+----------+
| Fail     |      511 |
+----------+----------+
| Success  |      489 |
+==========+==========+
<BLANKLINE>
## Fail Chains
+==========+==========+
|   len    |  Count   |
+----------+----------+
| 1        |      104 |
+----------+----------+
...
+----------+----------+
| 34       |        1 |
+==========+==========+
<BLANKLINE>
## Success Chains
+==========+==========+
|   len    |  Count   |
+----------+----------+
| 1        |      210 |
+----------+----------+
...
+----------+----------+
| 24       |        1 |
+==========+==========+
<BLANKLINE>
<BLANKLINE>
"""


# End of Controlling complex sequences of steps

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
