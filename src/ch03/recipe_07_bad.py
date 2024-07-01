# Python Cookbook, 3rd Ed.
#
# Chapter: Function Definitions
# Recipe: Writing hints for more complex types

def temperature_bad(
    *,
    f_temp: float | None = None,
    c_temp: float | None = None
) -> float:

    if f_temp is not None:
        c_temp = 5 * (f_temp - 32) / 9
    elif f_temp is not None:
        f_temp = 32 + 9 * c_temp / 5
    else:
        raise TypeError("One of f_temp or c_temp must be provided")
    result = {"c_temp": c_temp, "f_temp": f_temp}
    return result
