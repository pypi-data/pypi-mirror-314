"""
This script provides a function to convert speed between different units of measurement.

The `speed_converter` function accepts a speed and converts it from one unit to another using predefined conversion formulas. 
It supports a range of speed units including meters per second, kilometers per hour, miles per hour, and knots. The conversion is performed by leveraging 
the `speed_formulas` module, which contains specific methods for handling each speed unit.

### Supported Units:
- "meters_per_second" (m/s)
- "kilometers_per_hour" (km/h)
- "miles_per_hour" (mph)
- "knots" (kn)

### Main Function:
- `speed_converter(speed: float, from_unit: str, to_unit: str, with_unit: bool = False, rounded_result: bool = False, humanized_input: bool = False) -> Union[float, str]`

  Converts the input speed (`speed`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result. The `rounded_result` parameter controls whether the result should be rounded.

### Example Usage:
- Converting 20 meters per second (m/s) to kilometers per hour (km/h):
    ```python
    speed_converter(20, "meters_per_second", "kilometers_per_hour")
    ```
- Converting 20 meters per second (m/s) to kilometers per hour (km/h) with the unit in the result:
    ```python
    speed_converter(20, "meters_per_second", "kilometers_per_hour", with_unit=True)
    ```
- Converting 20 meters per second (m/s) to kilometers per hour (km/h) with rounding enabled:
    ```python
    speed_converter(20, "meters_per_second", "kilometers_per_hour", rounded_result=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `speed_formulas` module from the `formulas` package to perform the actual conversion operations.
"""

from typing import Union
from Metricus._formulas import speed_formulas as sf
from Metricus.utilities import round_number, humanize_input

unit_list = {
    "m/s": ["meter_per_second", "m/s"],
    "km/h": ["kilometer_per_hour", "km/h"],
    "mph": ["mile_per_hour", "mph"],
    "kn": ["knot", "kn"]
}


def speed_converter(
    speed: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given speed from one unit to another.

    Args:
        speed (float): The speed to be converted.
        from_unit (str): The unit of the speed to convert from.
        to_unit (str): The unit to convert the speed to.
        rounded_result (bool, optional): If True, the result will be rounded. Defaults to False.
        humanized_input (bool, optional): If True, the input units are humanized (e.g., 'meter per second' instead of 'meter_per_second'). Defaults to False.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted speed. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted speed.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `speed_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        speed_converter(20, "meters_per_second", "kilometers_per_hour")  # Converts 20 m/s to km/h
        speed_converter(20, "meters_per_second", "kilometers_per_hour", with_unit=True)  # Converts 20 m/s to km/h and includes the unit in the result
        speed_converter(20, "meters_per_second", "kilometers_per_hour", rounded_result=True)  # Converts 20 m/s to km/h with rounding enabled
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    # Normalize the input to the unit abbreviation
    from_unit = next((unit for unit, names in unit_list.items() if from_unit.lower() in [name.lower() for name in names]), from_unit)
    to_unit = next((unit for unit, names in unit_list.items() if to_unit.lower() in [name.lower() for name in names]), to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    if from_unit == to_unit:
        result = round_number(speed) if rounded_result else speed
    elif from_unit == "m/s":
        result = sf.MetersPerSecond(speed, with_unit=with_unit).mps_to(to_unit)
    elif from_unit == "km/h":
        result = sf.KilometersPerHour(speed, with_unit=with_unit).kmph_to(to_unit)
    elif from_unit == "mph":
        result = sf.MilesPerHour(speed, with_unit=with_unit).mph_to(to_unit)
    elif from_unit == "kn":
        result = sf.Knots(speed, with_unit=with_unit).kn_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
