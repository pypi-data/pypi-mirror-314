"""
This script provides a function to convert forces between different units of measurement.

The `force_converter` function accepts a force value and converts it from one unit to another using predefined conversion formulas.
It supports a variety of units related to force, including newton, pound force, and other common units.
The conversion is performed by leveraging the `force_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- "newton" (N)
- "dyne" (dyn)
- "kilonewton" (kN)
- "pound_force" (lbf)
- "ounce_force" (ozf)
- "ton_force" (tonf)
- "kilogram_force" (kgf)
- "gram_force" (gf)
- "millinewton" (mN)
- "poundal" (pdl)
- "slug_force" (slf)

### Main Function:
- `force_converter(force: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]`

  Converts the input force (`force`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `with_unit` parameter allows for an optional
  string output that includes the unit in the result. If `humanized_input` is set to True, the input units can be written in a more 
  user-friendly format (e.g., "pound force" instead of "pound_force").

### Example Usage:
- Converting 10 newtons (N) to pound-force (lbf):
    ```python
    force_converter(10, "newton", "pound_force")
    ```
- Converting 10 newtons (N) to pound-force (lbf) with the unit in the result:
    ```python
    force_converter(10, "newton", "pound_force", True)
    ```

- Converting with humanized input:
    ```python
    force_converter(10, "pound force", "kilonewton", humanized_input=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

Dependencies:
- The script uses the `force_formulas` module from the `formulas` package to perform the actual conversion operations.
"""

from typing import Union

from Metricus._formulas import force_formulas as ff
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "newton",
    "dyne",
    "kilonewton",
    "pound_force",
    "ounce_force",
    "ton_force",
    "kilogram_force",
    "gram_force",
    "millinewton",
    "poundal",
    "slug_force",
]


def force_converter(
    force: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts the input force from a given unit to another.

    Args:
        force (float): The force value to be converted.
        from_unit (str): The unit of force to convert from.
        to_unit (str): The unit to convert the force to.
        rounded_result (bool, optional): If True, the result will be rounded to the nearest integer. Defaults to False.
        humanized_input (bool, optional): If True, the input units are processed with a human-friendly format (e.g., "pound force"). Defaults to False.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted force. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted force.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    Example usage:
        force_converter(10, "newton", "pound_force")  # Converts 10 N to lbf
        force_converter(10, "newton", "pound_force", with_unit=True)  # Converts 10 N to lbf and includes the unit in the result
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(force) if rounded_result else force
    elif from_unit == "newton":
        result = ff.Newton(force, with_unit=with_unit).newton_to(to_unit)
    elif from_unit == "dyne":
        result = ff.Dyne(force, with_unit=with_unit).dyne_to(to_unit)
    elif from_unit == "kilonewton":
        result = ff.Kilonewton(force, with_unit=with_unit).kilonewton_to(to_unit)
    elif from_unit == "pound_force":
        result = ff.PoundForce(force, with_unit=with_unit).pound_force_to(to_unit)
    elif from_unit == "ounce_force":
        result = ff.OunceForce(force, with_unit=with_unit).ounce_force_to(to_unit)
    elif from_unit == "ton_force":
        result = ff.TonForce(force, with_unit=with_unit).ton_force_to(to_unit)
    elif from_unit == "kilogram_force":
        result = ff.KilogramForce(force, with_unit=with_unit).kilogram_force_to(to_unit)
    elif from_unit == "gram_force":
        result = ff.GramForce(force, with_unit=with_unit).gram_force_to(to_unit)
    elif from_unit == "millinewton":
        result = ff.Millinewton(force, with_unit=with_unit).millinewton_to(to_unit)
    elif from_unit == "poundal":
        result = ff.Poundal(force, with_unit=with_unit).poundal_to(to_unit)
    elif from_unit == "slug_force":
        result = ff.SlugForce(force, with_unit=with_unit).slug_force_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
