# Exploration

This notebook shows some basic exploration of Jupyter Lab features.


```python
from matplotlib import pyplot as plt
from pydantic import BaseModel
```

## Bad Code example

This shows how the notebook behaves when use set the `raises-exception` Cell Tag.


```python
bad code
```


      Cell In[2], line 1
        bad code
            ^
    SyntaxError: invalid syntax




```python
print("good code")
```

    good code



```python
value = 355/113
assert value == 3.14, f"invald {value}"
```


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    Cell In[4], line 2
          1 value = 355/113
    ----> 2 assert value == 3.14, f"invald {value}"


    AssertionError: invald 3.1415929203539825



```python

```
