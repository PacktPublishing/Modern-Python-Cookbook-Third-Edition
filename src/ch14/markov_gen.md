# Python Cookbook, 3rd Ed.

Chapter 14, Application Integration: Combination

Markov Generator



```python
from collections.abc import Callable
from typing import TypeAlias, Any
import random
from functools import partial
```


```python
Chain: TypeAlias = list[int]
State: TypeAlias = Callable[[Chain, int], tuple[Chain, Any]]
```


```python
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
```


```python
class Dice:
    def __init__(self, seed=None) -> None:
        self._rng = random.Random(seed)
        self.roll()
    def roll(self) -> tuple[int, ...]:
        self.dice = (
            self._rng.randint(1, 6),
            self._rng.randint(1, 6))
        return self.dice
```


```python
def generate(dice: Dice) -> tuple[str, Chain]:
    state, chain = start, []
    try:
        while True:
            roll = sum(dice.roll())
            chain, state = state(chain, roll)
    except Succeed:
        return ("Success", chain)
    except Fail:
        return ("Fail", chain)

```

## Test


```python
d = Dice(1337)

for i in range(10):
    print(generate(d))
```

    ('Fail', [9, 10, 8, 7])
    ('Success', [7])
    ('Fail', [9, 5, 10, 6, 12, 7])
    ('Success', [9, 4, 6, 6, 5, 12, 9])
    ('Success', [7])
    ('Fail', [10, 6, 5, 11, 7])
    ('Success', [4, 4])
    ('Success', [11])
    ('Fail', [8, 9, 7])
    ('Fail', [12])


## Output


```python
from argparse import Namespace
from contextlib import redirect_stdout
import csv
from pathlib import Path
import sys
from typing import TextIO
```


```python
class Writer:
    def __init__(self, target: TextIO = sys.stdout) -> None:
        self.target = target
    def header(self, opts: Namespace, columns: bool=True) -> None:
        ...
    def sample(self, outcome: str, chain: list[int]) -> None:
        ...
```


```python
class CSVWriter(Writer):
    def __init__(self, target: TextIO) -> None:
        super().__init__(target)
    def header(self, opts: Namespace, columns: bool = True) -> None:
        with redirect_stdout(self.target):
            print(f'# file = "{opts.file_name}"')
            print(f'# samples = {opts.sample_count}')
            print(f'# randomize = {opts.randomize}')
        if columns:
            with redirect_stdout(self.target):
                print('# -----')
            self.target.flush()
            self.writer = csv.writer(self.target)
            self.writer.writerow(['outcome', 'length','chain'])
    def sample(self, outcome: str, chain: list[int]) -> None:
        self.writer.writerow([outcome, len(chain), ';'.join(map(str, chain))])
```


```python
class TOMLWriter(Writer):
    def header(self, opts: Namespace, columns: bool = True) -> None:
        with redirect_stdout(self.target):
            print("[Configuration]")
            print(f'  file = "{opts.file_name}"')
            print(f'  samples = {opts.sample_count}')
            print(f'  randomize = {opts.randomize}')
    def sample(self, outcome: str, chain: list[int]) -> None:
        with redirect_stdout(self.target):
            print("[[Samples]]")
            print(f'  outcome = "{outcome}"')
            print(f'  length = {len(chain)}')
            print(f'  chain = {chain}')
```


```python
opts = Namespace(
    file_name = "sample.csv",
    sample_count = 100,
    randomize = 42
)

dice = Dice(opts.randomize)
target = Path("../../data") / "ch14" / opts.file_name

with target.open('w') as target_file:
    writer = CSVWriter(target_file)
    writer.header(opts, columns=True)
    for i in range(opts.sample_count):
        outcome, chain = generate(dice)
        writer.sample(outcome, chain)
```


```python

```
