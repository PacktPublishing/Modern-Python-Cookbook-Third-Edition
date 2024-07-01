# Anscombe's Quartet -- Core Computations

The raw data has four series.

We'll define a some classes and ingest the data.

Globals:

-  `quartet` has the quartet data that can be used for presentations.

## Imports


```python
import json
from pathlib import Path
import statistics

from pydantic import BaseModel
```

## Classes


```python
class Pair(BaseModel):
    x: float
    y: float

class Series(BaseModel):
    series: str
    data: list[Pair]

    @property
    def x(self) -> list[float]:
        return [p.x for p in self.data]
        
    @property
    def y(self) -> list[float]:
        return [p.y for p in self.data]

    @property
    def correlation(self) -> float:
        return statistics.correlation(self.x, self.y)

    @property
    def regression(self) -> tuple[float, float]:
        return statistics.linear_regression(self.x, self.y)
```


```python
from math import isclose
test = Series(
    series="test", 
    data=[Pair(x=2, y=4), Pair(x=3, y=6), Pair(x=5, y=10)]
)
assert isclose(test.correlation, 1.0)
assert isclose(test.regression.slope, 2.0)
assert isclose(test.regression.intercept, 0.0)
```

## Data Loading


```python
source = Path.cwd().parent.parent / "data" / "anscombe.json"
with source.open() as source_file:
    json_document = json.load(source_file)
    source_data = (Series.model_validate(s) for s in json_document)
    quartet = {s.series: s for s in source_data}
```


```python
quartet['I']
```


```python
quartet['IV']
```

## Statistical Computations


```python
quartet['I'].correlation
```


```python
r = quartet['I'].regression
f"y = {r.slope:.1f} * x + {r.intercept:.1f}"
```
