# Anscombe's Quartet

The raw data has four series. We'll ingest the data in several forms

## Raw Data for the Series


```python
import json
from pathlib import Path
from pydantic import BaseModel
```


```python
source_path = Path.cwd().parent.parent / "data" / "anscombe.json"
with source_path.open() as source_file:
    all_data = json.load(source_file)
[data['series'] for data in all_data]
```




    ['I', 'II', 'III', 'IV']




```python
all_data[0]['data']
```




    [{'x': 10.0, 'y': 8.04},
     {'x': 8.0, 'y': 6.95},
     {'x': 13.0, 'y': 7.58},
     {'x': 9.0, 'y': 8.81},
     {'x': 11.0, 'y': 8.33},
     {'x': 14.0, 'y': 9.96},
     {'x': 6.0, 'y': 7.24},
     {'x': 4.0, 'y': 4.26},
     {'x': 12.0, 'y': 10.84},
     {'x': 7.0, 'y': 4.82},
     {'x': 5.0, 'y': 5.68}]



## Pydantic Model


```python
from pydantic import BaseModel
```


```python
class Pair(BaseModel):
    x: float
    y: float

class Series(BaseModel):
    series: str
    data: list[Pair]
```


```python
clean_data = [Series.model_validate(d) for d in all_data]
```


```python
clean_data[0]
```




    Series(series='I', data=[Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95), Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81), Pair(x=11.0, y=8.33), Pair(x=14.0, y=9.96), Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26), Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82), Pair(x=5.0, y=5.68)])




```python
clean_data[1]
```




    Series(series='II', data=[Pair(x=10.0, y=9.14), Pair(x=8.0, y=8.14), Pair(x=13.0, y=8.74), Pair(x=9.0, y=8.77), Pair(x=11.0, y=9.26), Pair(x=14.0, y=8.1), Pair(x=6.0, y=6.13), Pair(x=4.0, y=3.1), Pair(x=12.0, y=9.13), Pair(x=7.0, y=7.26), Pair(x=5.0, y=4.74)])




```python
quartet = {s.series: s for s in clean_data}
```


```python
quartet['I']
```




    Series(series='I', data=[Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95), Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81), Pair(x=11.0, y=8.33), Pair(x=14.0, y=9.96), Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26), Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82), Pair(x=5.0, y=5.68)])




```python
quartet.keys()
```




    dict_keys(['I', 'II', 'III', 'IV'])



## Revised Design

This is a more focused data loading cell.


```python
source_path = Path.cwd().parent.parent / "data" / "anscombe.json"
with source_path.open() as source_file:
    json_document = json.load(source_file)
    source_data = (Series.model_validate(s) for s in json_document)
    quartet = {s.series: s for s in source_data}
```


```python
quartet
```


```python
for name in quartet:
    print(f"{name:3s} {len(quartet[name].data):d}")
```


```python

```
