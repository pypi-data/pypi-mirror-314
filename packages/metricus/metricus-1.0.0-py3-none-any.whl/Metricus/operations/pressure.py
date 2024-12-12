"""
This script provides a function to convert pressure between different units of measurement.

The `pressure_converter` function accepts a pressure value and converts it from one unit to another using predefined conversion formulas. 
It supports a variety of pressure units, including Pascal, millimeters of mercury, pound force per square inch, bar, and atmosphere. 
The conversion is performed by leveraging the `pressure_formulas` module, which contains specific methods for handling each pressure unit.

### Supported Units:
- "pascal" (Pa)
- "mmHg" (mmHg)
- "psi" (psi)
- "bar" (bar)
- "atmosphere" (atm)

### Main Function:
- `pressure_converter(pressure: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]`

  Converts the input pressure (`pressure`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `rounded_result` parameter determines if the result should be rounded, 
  and the `humanized_input` allows users to input units in a more user-friendly format (e.g., "Pascal" instead of "pascal"). 
  The `with_unit` parameter allows for an optional string output that includes the unit in the result.

### Example Usage:
- Converting 101325 pascals (Pa) to atmospheres (atm):
    ```python
    pressure_converter(101325, "pascal", "atmosphere")
    ```

- Converting 101325 pascals (Pa) to atmospheres (atm) with the unit in the result:
    ```python
    pressure_converter(101325, "pascal", "atmosphere", with_unit=True)
    ```

- Converting 101325 pascals (Pa) to atmospheres (atm) with the unit in the result and rounding the result:
    ```python
    pressure_converter(101325, "pascal", "atmosphere", with_unit=True, rounded_result=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `pressure_formulas` module from the `formulas` package to perform the actual conversion operations.
"""

from typing import Union

from Metricus._formulas import pressure_formulas as pf
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "pascal",
    "mmHg",
    "psi",
    "bar",
    "atmosphere",
]


def pressure_converter(
    pressure: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given pressure from one unit to another.

    Args:
        pressure (float): The pressure to be converted.
        from_unit (str): The unit of the pressure to convert from.
        to_unit (str): The unit to convert the pressure to.
        rounded_result (bool, optional): If True, the result will be rounded to the nearest integer. Defaults to False.
        humanized_input (bool, optional): If True, the input units will be converted to a more user-friendly format (e.g., "Pascal" instead of "pascal"). Defaults to False.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted pressure. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted pressure.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `pressure_formulas` module from the `formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        pressure_converter(101325, "pascal", "atmosphere")  # Converts 101325 pascals to atmospheres
        pressure_converter(101325, "pascal", "atmosphere", with_unit=True)  # Converts 101325 pascals to atmospheres and includes the unit in the result
        pressure_converter(101325, "pascal", "atmosphere", rounded_result=True, with_unit=True)  # Converts 101325 pascals to atmospheres, includes the unit in the result, and rounds the value
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)
        if from_unit == "mmhg":
            from_unit = "mmHg"
        if to_unit == "mmhg":
            to_unit = "mmHg"

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(pressure) if rounded_result else pressure
    elif from_unit == "pascal":
        result = pf.Pascal(pressure, with_unit=with_unit).pascal_to(to_unit)
    elif from_unit == "mmHg":
        result = pf.MillimeterOfMercury(
            pressure, with_unit=with_unit
        ).mmHg_to(to_unit)
    elif from_unit == "psi":
        result = pf.PoundForcePerSquareInch(
            pressure, with_unit=with_unit
        ).psi_to(to_unit)
    elif from_unit == "bar":
        result = pf.Bar(pressure, with_unit=with_unit).bar_to(to_unit)
    elif from_unit == "atmosphere":
        result = pf.Atmosphere(pressure, with_unit=with_unit).atmosphere_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
