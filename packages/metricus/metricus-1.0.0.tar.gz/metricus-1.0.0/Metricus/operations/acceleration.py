"""
This script provides a function to convert accelerations between different units of measurement.

The `acceleration_converter` function accepts an acceleration value and converts it from one unit to another using predefined conversion formulas.
It supports a variety of units related to acceleration, including meters per second squared, feet per second squared, and other common units.
The conversion is performed by leveraging the `acceleration_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- "meter_per_second_squared" (m/s²)
- "foot_per_second_squared" (ft/s²)
- "centimeter_per_second_squared" (cm/s²)
- "gal" (gal)
- "inch_per_second_squared" (in/s²)
- "kilometer_per_hour_squared" (km/h²)
- "mile_per_hour_squared" (mi/h²)
- "gravity" (g)

### Main Function:
- `acceleration_converter(acceleration: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]`

  Converts the input acceleration (`acceleration`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The parameters include options for rounding the result,
  handling human-readable unit inputs, and including the unit in the result.

### Parameters:
- `acceleration` (float): The numeric value of acceleration to be converted.
- `from_unit` (str): The unit of acceleration to convert from. Must be one of the supported units.
- `to_unit` (str): The unit of acceleration to convert to. Must be one of the supported units.
- `rounded_result` (bool, optional): If True, rounds the output to a standard number of decimal places. Defaults to False.
- `humanized_input` (bool, optional): If True, normalizes unit strings to handle various input styles, such as replacing spaces with underscores. Defaults to False.
- `with_unit` (bool, optional): If True, appends the unit to the output as part of the result. Defaults to False.

### Returns:
- Union[float, str]: The converted acceleration value. If `with_unit` is True, the result includes the unit as a string; otherwise, it is a float.

### Example Usage:
1. Converting 9.8 m/s² to ft/s²:
    ```python
    acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared")
    ```
2. Converting 9.8 m/s² to ft/s² with the unit included:
    ```python
    acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared", with_unit=True)
    ```
3. Handling humanized input and rounding the result:
    ```python
    acceleration_converter(9.8, "Meter per Second Squared", "foot per second squared", rounded_result=True, humanized_input=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError` with an appropriate message.

Dependencies:
- The script uses the `acceleration_formulas` module from the `Metricus._formulas` package for specific unit conversion logic.
- Helper utilities like `round_number` and `humanize_input` are also utilized.

Notes:
- The `humanize_input` parameter allows the user to provide units in a more readable format, such as "meter per second squared" instead of "meter_per_second_squared".
"""

from typing import Union
from Metricus._formulas import acceleration_formulas as acf
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "meter_per_second_squared",
    "foot_per_second_squared",
    "centimeter_per_second_squared",
    "gal",
    "inch_per_second_squared",
    "kilometer_per_hour_squared",
    "mile_per_hour_squared",
    "gravity",
]


def acceleration_converter(
    acceleration: float,
    from_unit: str,
    to_unit: str,
    rounded_result: bool = False,
    humanized_input: bool = False,
    with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given acceleration from one unit to another.

    Args:
        acceleration (float): The acceleration value to be converted.
        from_unit (str): The unit of acceleration to convert from.
        to_unit (str): The unit to convert the acceleration to.
        rounded_result (bool, optional): If True, rounds the result. Defaults to False.
        humanized_input (bool, optional): If True, normalizes input unit names. Defaults to False.
        with_unit (bool, optional): If True, appends the unit to the result. Defaults to False.

    Returns:
        Union[float, str]: The converted acceleration value. If `with_unit` is True, the result includes the unit; otherwise, it is a float.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized.

    Example usage:
        acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared")
        acceleration_converter(9.8, "meter_per_second_squared", "foot_per_second_squared", with_unit=True)
    """
    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)
    
    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(acceleration) if rounded_result else acceleration
    elif from_unit == "meter_per_second_squared":
        result = acf.MeterPerSecondSquared(acceleration, with_unit=with_unit).mps2_to(
            to_unit
        )
    elif from_unit == "foot_per_second_squared":
        result = acf.FootPerSecondSquared(acceleration, with_unit=with_unit).fps2_to(
            to_unit
        )
    elif from_unit == "centimeter_per_second_squared":
        result = acf.CentimeterPerSecondSquared(
            acceleration, with_unit=with_unit
        ).cmps2_to(to_unit)
    elif from_unit == "gal":
        result = acf.Gal(acceleration, with_unit=with_unit).gal_to(to_unit)
    elif from_unit == "inch_per_second_squared":
        result = acf.InchPerSecondSquared(acceleration, with_unit=with_unit).ips2_to(
            to_unit
        )
    elif from_unit == "kilometer_per_hour_squared":
        result = acf.KilometerPerHourSquared(acceleration, with_unit=with_unit).kmh2_to(
            to_unit
        )
    elif from_unit == "mile_per_hour_squared":
        result = acf.MilePerHourSquared(acceleration, with_unit=with_unit).mph2_to(
            to_unit
        )
    elif from_unit == "gravity":
        result = acf.Gravity(acceleration, with_unit=with_unit).g_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
