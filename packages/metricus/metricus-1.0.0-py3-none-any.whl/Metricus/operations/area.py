"""
This script provides a function to convert areas between different units of measurement.

The `area_converter` function accepts an area value and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of area units from both metric and imperial systems. The conversion process utilizes the `area_formulas` 
module, which includes specific methods for handling each type of unit.

### Supported Units:
- Metric:
  - "square_centimeter" (cm²)
  - "square_meter" (m²)
  - "hectare" (ha)
  - "square_kilometer" (km²)
- Imperial:
  - "square_foot" (ft²)
  - "square_yard" (yd²)
  - "acre" (ac)

### Main Function:
- `area_converter(area: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]`
  
  Converts the input area (`area`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function allows options for 
  rounding the result, handling human-readable unit names, and including the unit in the output.

### Parameters:
- `area` (float): The numeric value of the area to be converted.
- `from_unit` (str): The unit of the area to convert from. Must be one of the supported units.
- `to_unit` (str): The unit to convert the area to. Must be one of the supported units.
- `rounded_result` (bool, optional): If True, rounds the output to a standard number of decimal places. Defaults to False.
- `humanized_input` (bool, optional): If True, allows unit names to be entered in a more readable format (e.g., "square meter" instead of "square_meter"). Defaults to False.
- `with_unit` (bool, optional): If True, appends the unit to the output as part of the result. Defaults to False.

### Returns:
- Union[float, str]: The converted area value. If `with_unit` is True, the result includes the unit as a string; otherwise, it is a float.

### Example Usage:
1. Converting 100 square meters to hectares:
    ```python
    area_converter(100, "square_meter", "hectare")
    ```
2. Converting 1 acre to square meters with the unit in the result:
    ```python
    area_converter(1, "acre", "square_meter", with_unit=True)
    ```
3. Handling humanized input and rounding the result:
    ```python
    area_converter(1000, "Square Foot", "square_meter", rounded_result=True, humanized_input=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError` with an appropriate message.

### Dependencies:
- The script uses the `area_formulas` module from the `Metricus._formulas` package for specific conversion logic.
- Helper utilities like `round_number` and `humanize_input` are also utilized.

### Notes:
- The `humanize_input` parameter enables the user to input units in a more readable format, such as "square meter" instead of "square_meter".
"""

from typing import Union
from Metricus._formulas import area_formulas as af
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "square_centimeter",
    "square_foot",
    "square_meter",
    "square_yard",
    "acre",
    "hectare",
    "square_kilometer",
]


def area_converter(
    area: float,
    from_unit: str,
    to_unit: str,
    rounded_result: bool = False,
    humanized_input: bool = False,
    with_unit: bool = False,
) -> Union[float, str]:
    """
    Converts a given area from one unit to another.

    Args:
        area (float): The area to be converted.
        from_unit (str): The unit of the area to convert from. Must be one of the supported units in `unit_list`.
        to_unit (str): The unit to convert the area to. Must be one of the supported units in `unit_list`.
        rounded_result (bool, optional): If True, rounds the result. Defaults to False.
        humanized_input (bool, optional): If True, allows readable input unit names. Defaults to False.
        with_unit (bool, optional): If True, includes the unit in the output. Defaults to False.

    Returns:
        Union[float, str]: The converted area. If `with_unit` is True, includes the unit; otherwise, returns a float.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    Example usage:
        area_converter(100, "square_meter", "hectare")  # Converts 100 square meters to hectares
        area_converter(1, "acre", "square_meter", with_unit=True)  # Converts 1 acre to square meters with unit in the result
    """
    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    if from_unit == to_unit:
        result = round_number(area) if rounded_result else area
    elif from_unit == "square_centimeter":
        result = af.SquareCentimeter(area, with_unit=with_unit).square_centimeter_to(
            to_unit
        )
    elif from_unit == "square_foot":
        result = af.SquareFoot(area, with_unit=with_unit).square_foot_to(to_unit)
    elif from_unit == "square_meter":
        result = af.SquareMeter(area, with_unit=with_unit).square_meter_to(to_unit)
    elif from_unit == "square_yard":
        result = af.SquareYard(area, with_unit=with_unit).square_yard_to(to_unit)
    elif from_unit == "acre":
        result = af.Acre(area, with_unit=with_unit).acre_to(to_unit)
    elif from_unit == "hectare":
        result = af.Hectare(area, with_unit=with_unit).hectare_to(to_unit)
    elif from_unit == "square_kilometer":
        result = af.SquareKilometer(
            area, with_unit=with_unit
        ).square_kilometer_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")

    return round_number(result) if rounded_result else result
