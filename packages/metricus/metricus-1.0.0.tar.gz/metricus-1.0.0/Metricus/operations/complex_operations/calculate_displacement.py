"""
This module provides a function to calculate the time required to travel a given 
distance at a specified speed, using various units for distance, speed, and time.

Function:
    - calculate_displacement: A function that calculates the time required to 
      travel a specified distance at a given speed, with support for converting 
      between different units for distance, speed, and time. The time can be returned 
      either as a numeric value or as a string with the unit included.

Units Supported for Conversion:
    - Length Units:
        - 'kilometer': Kilometer, the base unit for length in this function.
        - 'meter': Meter, a unit of length equal to 1000 meters in a kilometer.
        - 'mile': Mile, a unit of length used in the imperial system.
        - 'yard': Yard, a unit of length used in the imperial system.
        - 'foot': Foot, a unit of length used in the imperial system.
        - 'inch': Inch, a unit of length used in the imperial system.
        - Other standard length units may also be supported depending on the context.
    - Speed Units:
        - 'km/h': Kilometer per hour, the base unit for speed in this function.
        - 'm/s': Meter per second, a unit of speed.
        - 'mile/h': Miles per hour, a unit of speed used in the imperial system.
        - 'foot/s': Feet per second, a unit of speed used in the imperial system.
        - Additional speed units may be supported based on specific use cases.
    - Time Units:
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
    - length (float): The distance traveled in the specified length unit.
    - speed (float): The speed in the specified speed unit.
    - time_unit (str, optional): The desired unit for the resulting time. Supported units are:
      'millisecond', 'minute', 'second', 'hour', 'day', 'week', 'month', 'year', 
      'decade', 'century'. Defaults to 'hour'.
    - length_unit (str, optional): The unit of the distance to convert to 'kilometer'. 
      Supported units are 'kilometer', 'meter', 'mile', 'yard', 'foot', and 'inch'. Defaults to 'kilometer'.
    - speed_unit (str, optional): The unit of speed to convert to 'km/h'. Supported units are:
      'km/h', 'm/s', 'mile/h', and 'foot/s'. Defaults to 'km/h'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, 
      which returns just the numeric value.
    - rounded_result (bool, optional): If True, the result will be rounded. Defaults to False.

Returns:
    - Union[float, str]: The calculated time required to travel the given distance, in the specified 
      unit. The result is returned as a float if `with_unit` is False, or as a string with the unit 
      if `with_unit` is True.

Raises:
    - ValueError: If any of the specified units for length, speed, or time are not recognized.

Usage Example:
    # Calculate the time to travel 100 meters at 5 meters per second, and convert it to hours
    result = calculate_displacement(100, 5, 'hour', 'meter', 'm/s')
    print(result)  # Output: 0.02

    # Calculate the time to travel 100 miles at 60 miles per hour, and include the unit in the result
    result = calculate_displacement(100, 60, 'minute', 'mile', 'mile/h', True)
    print(result)  # Output: "100.0 min"

    # Handle an unknown unit (will raise a ValueError)
    result = calculate_displacement(100, 60, 'unknown_unit', 'mile', 'mile/h')
    # Raises ValueError: The measurement has an unknown unit: unknown_unit
"""

from typing import Union

from Metricus._formulas.complex_formulas import displacement_calculator
from Metricus.operations import length as len
from Metricus.operations import speed as sp
from Metricus.utilities import round_number

dc = displacement_calculator.displacement_calculator


def calculate_displacement(
    length: float,
    speed: float,
    time_unit: str = "hour",
    length_unit: str = "kilometer",
    speed_unit: str = "km/h",
    rounded_result: bool = False,
    with_unit: bool = False,
) -> Union[float, str]:
    """
    Calculates the displacement based on the provided length, speed, and time.

    This function converts the provided length and speed to their respective units
    (kilometer and km/h), if necessary, and calculates the displacement using the
    `displacement_calculator` from the `formulas.complex_formulas` module. The result
    can optionally include the units of measurement.

    Args:
        length (float): The length value to be used in the calculation.
        speed (float): The speed value to be used in the calculation.
        time_unit (str, optional): The unit of time for the calculation. Default is 'hour'.
        length_unit (str, optional): The unit of length for the input value. Default is 'kilometer'.
        speed_unit (str, optional): The unit of speed for the input value. Default is 'km/h'.
        with_unit (bool, optional): If True, the result will include the unit. Default is False.
        rounded_result (bool, optional): If True, the result will be rounded. Default is False.

    Returns:
        Union[float, str]: The calculated displacement as a float if `with_unit` is False, or a string
                            with the result and unit if `with_unit` is True.

    Raises:
        ValueError: If an invalid unit is provided for length or speed.

    Example:
        >>> calculate_displacement(5, 60, time_unit='minute', length_unit='mile', speed_unit='mph', with_unit=True)
        '300.0 km'

    Notes:
        - The function first converts the length to kilometers and the speed to kilometers per hour,
          if necessary.
        - The `displacement_calculator` function is used to calculate the displacement based on
          the converted values.
        - The function supports custom units for time, length, and speed, with default units being
          'hour', 'kilometer', and 'km/h', respectively.
    """
    kilometer = (
        len.length_converter(length, length_unit, "kilometer")
        if length_unit != "kilometer"
        else length
    )

    kmh = (
        sp.speed_converter(speed, speed_unit, "km/h") if speed_unit != "km/h" else speed
    )

    result = dc(kilometer, kmh, time_unit=time_unit, with_unit=with_unit)
    return round_number(result) if rounded_result else result
