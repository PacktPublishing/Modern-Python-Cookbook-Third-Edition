# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Using super flexible keyword parameters


# Subsection: Getting ready

import warnings


# Subsection: How to do it...

def rtd_outline():

    if distance is None:
        distance = rate * time

    elif rate is None:
        rate = distance / time

    elif time is None:
        time = distance / rate

    else:
        warnings.warning("Nothing to solve for")

    return dict(distance=distance, rate=rate, time=time)

def rtd(
    distance: float | None = None,
    rate: float | None = None,
    time: float | None = None,
) -> dict[str, float | None]:

    if distance is None and rate is not None and time is not None:
        distance = rate * time
    elif rate is None and distance is not None and time is not None:
        rate = distance / time
    elif time is None and distance is not None and rate is not None:
        time = distance / rate
    else:
        warnings.warn("Nothing to solve for")

    return dict(distance=distance, rate=rate, time=time)

test_example1 = """
>>> rtd(distance=31.2, rate=6)
{'distance': 31.2, 'rate': 6, 'time': 5.2}

>>> result = rtd(distance=31.2, rate=6)

>>> ('At {rate}kt, it takes '
... '{time}hrs to cover {distance}nm').format_map(result)
'At 6kt, it takes 5.2hrs to cover 31.2nm'
"""

# Subsection: There's more...

def rtd2_draft(distance, rate, time, **kwargs):
    print(kwargs)

def rtd2(**keywords: float) -> dict[str, float | None]:

    rate = keywords.get('rate')
    time = keywords.get('time')
    distance = keywords.get('distance')

    # etc.
    if distance is None and rate is not None and time is not None:
        distance = rate * time
    elif rate is None and distance is not None and time is not None:
        rate = distance / time
    elif time is None and distance is not None and rate is not None:
        time = distance / rate
    else:
        warnings.warn("Nothing to solve for")

    return dict(distance=distance, rate=rate, time=time)


test_example2 = """
>>> rtd2(distnace=31.2, rate=6)
{'distance': None, 'rate': 6, 'time': None}
"""


def rtd3(**keywords: float) -> dict[str, float | None]:

    rate = keywords.pop("rate", None)
    time = keywords.pop("time", None)
    distance = keywords.pop("distance", None)
    if keywords:
        raise TypeError(
           f"Invalid keyword parameter: {''.join(keywords.keys())}")

    # etc.
    if distance is None and rate is not None and time is not None:
        distance = rate * time
    elif rate is None and distance is not None and time is not None:
        rate = distance / time
    elif time is None and distance is not None and rate is not None:
        time = distance / rate
    else:
        warnings.warn("Nothing to solve for")

    return dict(distance=distance, rate=rate, time=time)

test_error = """
>>> import warnings
>>> warnings.simplefilter('error')
>>> rtd(distance=31.2, rate=6, time=10)
Traceback (most recent call last):
...
UserWarning: Nothing to solve for

"""

# End of Using super flexible keyword parameters


__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
