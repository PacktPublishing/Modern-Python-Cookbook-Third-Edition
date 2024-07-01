Python Cookbook, 3rd Ed.

Chapter 14, Application Integration: Combination
Markov Summary



```python
from collections import Counter
import csv
from pathlib import Path
```


```python
outcome_counts = Counter()
lengths = {
    'Fail': Counter(),
    'Success': Counter(),
}
```


```python
for source in Path("../../data/ch14").glob("*.csv"):
    with source.open() as source_file:
        line_iter = iter(source_file)
        # Skip past the header
        for line in line_iter:
            if "-----" in line:
                break
            print(line.rstrip())
        reader = csv.DictReader(line_iter)
        for sample in reader:
            outcome_counts[sample['outcome']] += 1
            lengths[sample['outcome']][sample['length']] += 1
```

    # file = "sample.csv"
    # samples = 100
    # randomize = 42
    # file = "../../data/ch14/data.csv"
    # samples = 10
    # randomize = 0



```python
print(dict(outcome_counts))
for k, v in lengths.items():
    print((k, dict(v)))
```

    {'Success': 58, 'Fail': 52}
    ('Fail', {'2': 15, '5': 7, '4': 2, '1': 13, '3': 7, '7': 2, '6': 1, '8': 2, '11': 1, '10': 1, '9': 1})
    ('Success', {'1': 27, '3': 7, '2': 7, '7': 2, '6': 4, '4': 4, '12': 1, '5': 3, '8': 2, '14': 1})



```python
def tabulate(label: str, value: str, mapping: dict[str, int]) -> None:
    hline2 = f"+{'='*10}+{'='*10}+"
    hline1 = f"+{'-'*10}+{'-'*10}+"

    print(hline2)
    print(f"| {label:^8s} | {value:^8s} |")
    for k, v in sorted(mapping.items()):
        print(hline1)
        print(f"| {str(k):<8s} | {v:>8d} |")
    print(hline2)
```


```python
tabulate("Outcome", "Count", outcome_counts)
```

    +==========+==========+
    | Outcome  |  Count   |
    +----------+----------+
    | Fail     |       52 |
    +----------+----------+
    | Success  |       58 |
    +==========+==========+



```python
print("## Fail Chains")
tabulate("len", "Count", lengths["Fail"])
print()
print("## Success Chains")
tabulate("len", "Count", lengths["Success"])
print()
```

    ## Fail Chains
    +==========+==========+
    |   len    |  Count   |
    +----------+----------+
    | 1        |       13 |
    +----------+----------+
    | 10       |        1 |
    +----------+----------+
    | 11       |        1 |
    +----------+----------+
    | 2        |       15 |
    +----------+----------+
    | 3        |        7 |
    +----------+----------+
    | 4        |        2 |
    +----------+----------+
    | 5        |        7 |
    +----------+----------+
    | 6        |        1 |
    +----------+----------+
    | 7        |        2 |
    +----------+----------+
    | 8        |        2 |
    +----------+----------+
    | 9        |        1 |
    +==========+==========+
    
    ## Success Chains
    +==========+==========+
    |   len    |  Count   |
    +----------+----------+
    | 1        |       27 |
    +----------+----------+
    | 12       |        1 |
    +----------+----------+
    | 14       |        1 |
    +----------+----------+
    | 2        |        7 |
    +----------+----------+
    | 3        |        7 |
    +----------+----------+
    | 4        |        4 |
    +----------+----------+
    | 5        |        3 |
    +----------+----------+
    | 6        |        4 |
    +----------+----------+
    | 7        |        2 |
    +----------+----------+
    | 8        |        2 |
    +==========+==========+
    



```python

```


```python

```
