"""
This script provides a function to convert lengths between different units of measurement.

The length_converter function accepts a length value and converts it from one unit to another using predefined conversion formulas. 
It supports a variety of length units, including millimeters, centimeters, inches, feet, yards, meters, kilometers, miles, and nautical miles. The conversion is performed by leveraging 
the length_formulas module, which contains specific methods for handling each length unit.

### Supported Units:
- "millimeter" (mm)
- "centimeter" (cm)
- "inch" (in)
- "foot" (ft)
- "yard" (yd)
- "meter" (m)
- "kilometer" (km)
- "mile" (mi)
- "nautical_mile" (nm)

### Main Function:
- length_converter(length: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]

  Converts the input length (length) from a given unit (from_unit) to a target unit (to_unit). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The with_unit parameter allows for an optional
  string output that includes the unit in the result. The humanized_input parameter allows the user to input unit names in a more natural form, like "nautical mile" instead of "nautical_mile". 
  The rounded_result parameter allows for rounding the result to a specific decimal place.

### Example Usage:
- Converting 10 millimeters (mm) to centimeters (cm):
    
python
    length_converter(10, "millimeter", "centimeter")

- Converting 10 millimeters (mm) to centimeters (cm) with the unit in the result:
    
python
    length_converter(10, "millimeter", "centimeter", with_unit=True)

- Converting 10 millimeters (mm) to centimeters (cm) with rounded result:
    
python
    length_converter(10, "millimeter", "centimeter", rounded_result=True)

### Error Handling:
- If either from_unit or to_unit is not recognized (i.e., not in the supported unit_list), the function raises a ValueError.

Dependencies:
- The script uses the length_formulas module from the formulas package to perform the actual conversion operations.
"""

from typing import Union

from Metricus._formulas import length_formulas as lf
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "millimeter",
    "centimeter",
    "inch",
    "foot",
    "yard",
    "meter",
    "kilometer",
    "mile",
    "nautical_mile",
]


def length_converter(
    length: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given length from one unit to another.

    Args:
        length (float): The length to be converted.
        from_unit (str): The unit of the length to convert from.
        to_unit (str): The unit to convert the length to.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.
        rounded_result (bool, optional): If True, the result will be rounded to a specific decimal place. Defaults to False.
        humanized_input (bool, optional): If True, the function will accept human-readable input for unit names (e.g., "nautical mile"). Defaults to False.

    Returns:
        Union[float, str]: The converted length. If with_unit is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted length. The result may also be rounded
                           if rounded_result is set to True.

    Raises:
        ValueError: If either from_unit or to_unit is not recognized (not in unit_list).

    The function uses the length_formulas module from the formulas package to handle the actual conversions.
    The conversion process is determined based on the from_unit and to_unit parameters.

    Example usage:
        length_converter(10, "millimeter", "centimeter")  # Converts 10 millimeters to centimeters
        length_converter(10, "millimeter", "centimeter", with_unit=True)  # Converts 10 millimeters to centimeters and includes the unit in the result
        length_converter(10, "millimeter", "centimeter", rounded_result=True)  # Converts 10 millimeters to centimeters and rounds the result
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(length) if rounded_result else length
    elif from_unit == "millimeter":
        result = lf.Millimeter(length, with_unit=with_unit).millimeter_to(to_unit)
    elif from_unit == "centimeter":
        result = lf.Centimeter(length, with_unit=with_unit).centimeter_to(to_unit)
    elif from_unit == "inch":
        result = lf.Inch(length, with_unit=with_unit).inch_to(to_unit)
    elif from_unit == "foot":
        result = lf.Foot(length, with_unit=with_unit).foot_to(to_unit)
    elif from_unit == "yard":
        result = lf.Yard(length, with_unit=with_unit).yard_to(to_unit)
    elif from_unit == "meter":
        result = lf.Meter(length, with_unit=with_unit).meter_to(to_unit)
    elif from_unit == "kilometer":
        result = lf.Kilometer(length, with_unit=with_unit).kilometer_to(to_unit)
    elif from_unit == "mile":
        result = lf.Mile(length, with_unit=with_unit).mile_to(to_unit)
    elif from_unit == "nautical_mile":
        result = lf.NauticalMile(length, with_unit=with_unit).nautical_mile_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
