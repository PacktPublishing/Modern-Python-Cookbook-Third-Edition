# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Writing clear documentation strings with RST markup


# Subsection: Getting ready

def T_wc_0(T, V):
    """Wind Chill Temperature."""
    if V < 4.8 or T > 10.0:
        raise ValueError("V must be over 4.8 kph, T must be below 10°C")
    return 13.12 + 0.6215*T - 11.37*V**0.16 + 0.3965*T*V**0.16


# Subsection: How to do it...

def T_wc_1(T, V):
    """Computes the wind chill temperature."""
    ...

def T_wc_2(T, V):
    """Computes the wind chill temperature.
    The wind-chill, :math:`T_{wc}`,
    is based on air temperature, T, and wind speed, V.
    """
    ...

def T_wc_3(T: float, V: float):
    """Computes the wind chill temperature
    The wind-chill, :math:`T_{wc}`,
    is based on air temperature, T, and wind speed, V.

    :param T: Temperature in °C
    :param V: Wind Speed in kph
    """
    ...

def T_wc_4(T: float, V: float) -> float:
    """Computes the wind chill temperature
    The wind-chill, :math:`T_{wc}`,
    is based on air temperature, T, and wind speed, V.

    :param T: Temperature in °C
    :param V: Wind Speed in kph

    :returns: Wind-Chill temperature in °C
    """
    return 0.0  # Place-holder for mypy

def T_wc_5(T: float, V: float) -> float:
    """Computes the wind chill temperature
    The wind-chill, :math:`T_{wc}`,
    is based on air temperature, T, and wind speed, V.

    :param T: Temperature in °C
    :param V: Wind Speed in kph

    :returns: Wind-Chill temperature in °C

    :raises ValueError: for wind speeds under 4.8 kph or T above 10°C
    """
    return 0.0  # Place-holder for mypy

def T_wc(T: float, V: float) -> float:
    """Computes the wind chill temperature
    The wind-chill, :math:`T_{wc}`,
    is based on air temperature, T, and wind speed, V.

    :param T: Temperature in °C
    :param V: Wind Speed in kph

    :returns: Wind-Chill temperature in °C

    :raises ValueError: for wind speeds under 4.8 kph or T above 10°C

    >>> round(T_wc(-10, 25), 1)
    -18.8

    See https://en.wikipedia.org/wiki/Wind_chill
    .. math::

        T_{wc}(T_a, V) = 13.2 + 0.6215 T_a - 11.37 V ^ {0.16} + 0.3965 T_a V ^ {0.16}
    """
    if V < 4.8 or T > 10.0:
        raise ValueError("V must be over 4.8 kph, T must be below 10°C")
    return 13.12 + 0.6215*T - 11.37*V**0.16 + 0.3965*T*V**0.16

# Subsection: There's more...

def wind_chill_table() -> None:
    """Uses :func:`T_wc` to produce a wind-chill
    table for temperatures from -30°C to 10°C and
    wind speeds from 5kph to 50kph.
    """
    ... # etc.


# End of Writing clear documentation strings with RST markup
