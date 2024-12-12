"""
This module provides a function to calculate the time required to travel a given 
distance at a constant speed, and convert it to various units of time.

Function:
    - displacement_calculator: A function that calculates the time required to 
      travel a specified distance at a given speed, and converts the result to 
      the specified unit. The time can be returned either as a numeric value or 
      as a string with the unit included.

Units Supported for Conversion:
    - 'millisecond': Millisecond, a unit of time equal to one-thousandth of a second.
    - 'minute': Minute, a unit of time equal to 60 seconds.
    - 'second': Second, the base unit of time in the International System of Units.
    - 'hour': Hour, a unit of time equal to 60 minutes or 3600 seconds.
    - 'day': Day, a unit of time equal to 24 hours.
    - 'week': Week, a unit of time equal to 7 days.
    - 'month': Month, a unit of time based on the length of the month in the Gregorian calendar.
    - 'year': Year, a unit of time based on the length of the Earth's orbit around the sun.
    - 'decade': Decade, a unit of time equal to 10 years.
    - 'century': Century, a unit of time equal to 100 years.

Parameters:
    - kilometer (float): The distance traveled in kilometers.
    - kmh (float): The speed in kilometers per hour.
    - time_unit (str): The desired unit for the resulting time. Supported units are:
      'millisecond', 'minute', 'second', 'hour', 'day', 'week', 'month', 'year', 
      'decade', 'century'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, 
      which returns just the numeric value.

Returns:
    - Union[float, str]: The time required to travel the given distance, in the specified unit. 
      The result is returned as a float if `with_unit` is False, or as a string with the unit 
      if `with_unit` is True.

Raises:
    - ValueError: If the specified time unit is not recognized.

Usage Example:
    # Calculate the time to travel 100 kilometers at 50 km/h, and convert it to hours
    result = displacement_calculator(100, 50, 'hour')
    print(result)  # Output: 2.0

    # Calculate the time to travel 100 kilometers at 50 km/h, and include the unit in the result
    result = displacement_calculator(100, 50, 'minute', True)
    print(result)  # Output: "120.0 min"

    # Handle an unknown unit (will raise a ValueError)
    result = displacement_calculator(100, 50, 'unknown_unit')
    # Raises ValueError: The measurement has an unknown unit: unknown_unit
"""

from typing import Union

from Metricus\._formulas import time_formulas as tf


def displacement_calculator(
    kilometer: float, kmh: float, time_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Calculate the time required to travel a given distance at a constant speed.

    This function calculates the time required to travel a certain distance, given the distance in kilometers
    and speed in kilometers per hour. It allows the user to convert the result into different units of time
    such as hours, minutes, seconds, etc., using a provided time unit.

    Parameters:
    - kilometer (float): The distance traveled in kilometers.
    - kmh (float): The speed in kilometers per hour.
    - time_unit (str): The time unit to convert the result into. Supported units include:
      'millisecond', 'minute', 'second', 'hour', 'day', 'week', 'month', 'year', 'decade', 'century'.
    - with_unit (bool, optional): If True, the result is returned with the time unit. Defaults to False.

    Returns:
    - Union[float, str]: The time required to travel the given distance, in the specified time unit.
      The result can either be a numeric value (float) or a string (with the time unit attached if `with_unit=True`).

    Raises:
    - ValueError: If the provided `time_unit` is not recognized.

    Example:
    >>> displacement_calculator(100, 50, 'hour')
    2.0

    >>> displacement_calculator(100, 50, 'minute', with_unit=True)
    '120.0 min'

    >>> displacement_calculator(100, 50, 'day')
    0.08333333333333333

    """
    # Calculate the time in hours
    result = kilometer / kmh

    # If the time unit is hours, return the result directly or with the unit
    if time_unit == "hour":
        return f"{result} h" if with_unit else result

    # Define the supported time units
    units = [
        "millisecond",
        "minute",
        "second",
        "day",
        "week",
        "month",
        "year",
        "decade",
        "century",
    ]

    # If the time unit is valid, convert the result to the appropriate time unit
    if time_unit in units:
        return getattr(tf.Hour(result, with_unit=with_unit), "hour_to")(time_unit)

    # Raise an error if the time unit is not recognized
    raise ValueError(f"The measurement has an unknown unit: {time_unit}")
