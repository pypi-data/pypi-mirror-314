"""
This script provides a function to convert mass between different units of measurement.

The mass_converter function accepts a mass value and converts it from one unit to another using predefined conversion formulas. 
It supports a variety of mass units, including milligrams, carats, grams, ounces, pounds, kilograms, stones, slugs, and tonnes. 
The conversion is performed by leveraging the mass_formulas module, which contains specific methods for handling each mass unit.

### Supported Units:
- "milligram" (mg)
- "carat" (ct)
- "gram" (g)
- "ounce" (oz)
- "pound" (lb)
- "kilogram" (kg)
- "stone" (st)
- "slug" (sl)
- "tonne" (t)

### Main Function:
- mass_converter(mass: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]

  Converts the input mass (mass) from a given unit (from_unit) to a target unit (to_unit). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The `rounded_result` parameter determines if the result should be rounded, 
  and the `humanized_input` allows users to input units in a more user-friendly format (e.g., "Kilogram" instead of "kilogram"). 
  The `with_unit` parameter allows for an optional string output that includes the unit in the result.

### Example Usage:
- Converting 1000 milligrams (mg) to grams (g):

python
    mass_converter(1000, "milligram", "gram")

- Converting 1000 milligrams (mg) to grams (g) with the unit in the result:

python
    mass_converter(1000, "milligram", "gram", with_unit=True)

- Converting 1000 milligrams (mg) to grams (g) with the unit in the result and rounding the result:

python
    mass_converter(1000, "milligram", "gram", with_unit=True, rounded_result=True)

### Error Handling:
- If either from_unit or to_unit is not recognized (i.e., not in the supported unit_list), the function raises a ValueError.

Dependencies:
- The script uses the mass_formulas module from the formulas package to perform the actual conversion operations.
"""

from typing import Union

from Metricus._formulas import mass_formulas as mf
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "milligram",
    "carat",
    "gram",
    "ounce",
    "pound",
    "kilogram",
    "stone",
    "slug",
    "tonne",
]

def mass_converter(
    mass: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given mass from one unit to another.

    Args:
        mass (float): The mass to be converted.
        from_unit (str): The unit of the mass to convert from.
        to_unit (str): The unit to convert the mass to.
        rounded_result (bool, optional): If True, the result will be rounded to the nearest integer. Defaults to False.
        humanized_input (bool, optional): If True, the input units will be converted to a more user-friendly format (e.g., "Kilogram" instead of "kilogram"). Defaults to False.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted mass. If with_unit is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted mass.

    Raises:
        ValueError: If either from_unit or to_unit is not recognized (not in unit_list).

    The function uses the mass_formulas module from the formulas package to handle the actual conversions.
    The conversion process is determined based on the from_unit and to_unit parameters.

    Example usage:
        mass_converter(1000, "milligram", "gram")  # Converts 1000 milligrams to grams
        mass_converter(1000, "milligram", "gram", with_unit=True)  # Converts 1000 milligrams to grams and includes the unit in the result
        mass_converter(1000, "milligram", "gram", rounded_result=True, with_unit=True)  # Converts 1000 milligrams to grams, includes the unit in the result, and rounds the value
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(mass) if rounded_result else mass
    elif from_unit == "milligram":
        result = mf.Milligram(mass, with_unit=with_unit).milligram_to(to_unit)
    elif from_unit == "carat":
        result = mf.Carat(mass, with_unit=with_unit).carat_to(to_unit)
    elif from_unit == "gram":
        result = mf.Gram(mass, with_unit=with_unit).gram_to(to_unit)
    elif from_unit == "ounce":
        result = mf.Ounce(mass, with_unit=with_unit).ounce_to(to_unit)
    elif from_unit == "pound":
        result = mf.Pound(mass, with_unit=with_unit).pound_to(to_unit)
    elif from_unit == "kilogram":
        result = mf.Kilogram(mass, with_unit=with_unit).kilogram_to(to_unit)
    elif from_unit == "stone":
        result = mf.Stone(mass, with_unit=with_unit).stone_to(to_unit)
    elif from_unit == "slug":
        result = mf.Slug(mass, with_unit=with_unit).slug_to(to_unit)
    elif from_unit == "tonne":
        result = mf.Tonne(mass, with_unit=with_unit).tonne_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
