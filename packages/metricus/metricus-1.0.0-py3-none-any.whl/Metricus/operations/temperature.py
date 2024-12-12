"""
This script provides a function to convert temperatures between different units of measurement.

The `temperature_converter` function accepts a temperature and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of temperature units, including Celsius, Fahrenheit, Kelvin, and Rankine. The conversion is performed by leveraging 
the `temperature_formulas` module, which contains specific methods for handling each temperature unit.

### Supported Units:
- "celsius" (°C)
- "fahrenheit" (°F)
- "kelvin" (K)
- "rankine" (°R)

### Main Function:
- `temperature_converter(temp: float, from_unit: str, to_unit: str, with_unit: bool = False, rounded_result: bool = False, humanized_input: bool = False) -> Union[float, str]`

  Converts the input temperature (`temp`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result. The `rounded_result` parameter controls whether the result should be rounded.

### Example Usage:
- Converting 25 degrees Celsius (°C) to Fahrenheit (°F):
    ```python
    temperature_converter(25, "celsius", "fahrenheit")
    ```
- Converting 25 degrees Celsius (°C) to Fahrenheit (°F) with the unit in the result:
    ```python
    temperature_converter(25, "celsius", "fahrenheit", with_unit=True)
    ```
- Converting 25 degrees Celsius (°C) to Fahrenheit (°F) with rounding enabled:
    ```python
    temperature_converter(25, "celsius", "fahrenheit", False, rounded_result=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `temperature_formulas` module from the `formulas` package to perform the actual conversion operations.
"""

from typing import Union

from Metricus._formulas import temperature_formulas as tf
from Metricus.utilities import round_number, humanize_input

unit_list = ["celsius", "fahrenheit", "kelvin", "rankine"]


def temperature_converter(
    temp: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given temperature from one unit to another.

    Args:
        temp (float): The temperature to be converted.
        from_unit (str): The unit of the temperature to convert from.
        to_unit (str): The unit to convert the temperature to.
        rounded_result (bool, optional): If True, the result will be rounded. Defaults to False.
        humanized_input (bool, optional): If True, the input units are humanized (e.g., 'Celsius' instead of 'celsius'). Defaults to False.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted temperature. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted temperature.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `temperature_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        temperature_converter(25, "celsius", "fahrenheit")  # Converts 25 Celsius to Fahrenheit
        temperature_converter(25, "celsius", "fahrenheit", with_unit=True)  # Converts 25 Celsius to Fahrenheit and includes the unit in the result
        temperature_converter(25, "celsius", "fahrenheit", rounded_result=True)  # Converts 25 Celsius to Fahrenheit with rounding enabled
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(temp) if rounded_result else temp
    if from_unit == "celsius":
        result = tf.Celsius(temp, with_unit=with_unit).celsius_to(to_unit)
    elif from_unit == "fahrenheit":
        result = tf.Fahrenheit(temp, with_unit=with_unit).fahrenheit_to(to_unit)
    elif from_unit == "kelvin":
        result = tf.Kelvin(temp, with_unit=with_unit).kelvin_to(to_unit)
    elif from_unit == "rankine":
        result = tf.Rankine(temp, with_unit=with_unit).rankine_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
