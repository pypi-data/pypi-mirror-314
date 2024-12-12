"""
This script provides a function to convert volumes between different units of measurement.

The `volume_converter` function accepts a volume and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of units, including both metric and imperial systems. The conversion is performed by leveraging 
the `volume_formulas` module, which contains specific methods for handling each unit type.

### Supported Units:
- Metric: "mL" (Milliliters), "cm3" (Cubic Centimeters), "L" (Liters), "m3" (Cubic Meters)
- Imperial: "fl_oz" (Fluid Ounces), "cup" (Cups), "pt" (Pints), "qt" (Quarts), "gal" (Gallons), "bbl" (Barrels)
- Alternative representations: "cm³", "m³"

### Main Function:
- `volume_converter(volume: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]`
  
  Converts the input volume (`volume`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. Additional options allow for rounding the result,
  enabling human-readable input formats, and including the unit in the output.

### Parameters:
- `volume` (float): The volume value to be converted.
- `from_unit` (str): The source unit of the volume to convert from.
- `to_unit` (str): The target unit to convert the volume to.
- `rounded_result` (bool, optional): If True, rounds the result. Defaults to False.
- `humanized_input` (bool, optional): If True, allows human-readable unit input. Defaults to False.
- `with_unit` (bool, optional): If True, includes the unit of measurement in the result. Defaults to False.

### Example Usage:
- Converting 10 milliliters (mL) to liters (L):
    ```python
    volume_converter(10, "mL", "L")
    ```
- Converting 10 milliliters (mL) to liters (L) with the unit in the result:
    ```python
    volume_converter(10, "mL", "L", with_unit=True)
    ```
- Converting 10 fluid ounces to liters with human-readable input:
    ```python
    volume_converter(10, "Fluid Ounce", "Liter", humanized_input=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `valid_units`), the function raises a `ValueError`.

### Dependencies:
- The script uses the `volume_formulas` module from the `Metricus._formulas` package to perform the actual conversion operations.
- The `round_number` function is used for rounding results, and `humanize_input` allows for human-readable unit inputs.

"""

from typing import Union

from Metricus._formulas import volume_formulas as vf
from Metricus.utilities import round_number, humanize_input

unit_map = {
    "milliliter": "mL",
    "ml": "mL",
    "cubic_centimeter": "cm3",
    "cubic_centimetre": "cm³",
    "fluid_ounce": "fl_oz",
    "cup": "cup",
    "pint": "pt",
    "quart": "qt",
    "liter": "L",
    "litre": "L",
    "gallon": "gal",
    "barrel": "bbl",
    "cubic_meter": "m3",
    "cubic_metre": "m³",
    "l": "L",
}

valid_units = set(unit_map.values())
valid_units.update(unit_map.keys())

def normalize_unit(unit: str) -> str:
    unit = unit.lower()
    return unit_map.get(unit, unit)


def volume_converter(
    volume: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given volume from one unit to another.

    Args:
        volume (float): The volume to be converted.
        from_unit (str): The unit of the volume to convert from.
        to_unit (str): The unit to convert the volume to.
        rounded_result (bool, optional): If True, rounds the result. Defaults to False.
        humanized_input (bool, optional): If True, allows human-readable unit input. Defaults to False.
        with_unit (bool, optional): If True, includes the unit of measurement in the result. Defaults to False.

    Returns:
        Union[float, str]: The converted volume. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted volume.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `valid_units`).

    The function uses the `volume_formulas` module from the `Metricus._formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        volume_converter(10, "mL", "L")  # Converts 10 milliliters to liters
        volume_converter(10, "mL", "L", with_unit=True)  # Converts 10 milliliters to liters and includes the unit in the result
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    from_unit = normalize_unit(from_unit)
    to_unit = normalize_unit(to_unit)

    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(volume) if rounded_result else volume
    elif from_unit == "mL":
        result = vf.Milliliter(volume, with_unit=with_unit).mL_to(to_unit)
    elif from_unit in {"cm3", "cm³"}:
        result = vf.Milliliter(volume, with_unit=with_unit).mL_to(to_unit)
    elif from_unit == "fl_oz":
        result = vf.FluidOunce(volume, with_unit=with_unit).fl_oz_to(to_unit)
    elif from_unit == "cup":
        result = vf.Cup(volume, with_unit=with_unit).cup_to(to_unit)
    elif from_unit == "pt":
        result = vf.Pint(volume, with_unit=with_unit).pt_to(to_unit)
    elif from_unit == "qt":
        result = vf.Quart(volume, with_unit=with_unit).qt_to(to_unit)
    elif from_unit == "L":
        result = vf.Liter(volume, with_unit=with_unit).liter_to(to_unit)
    elif from_unit == "gal":
        result = vf.Gallon(volume, with_unit=with_unit).gal_to(to_unit)
    elif from_unit == "bbl":
        result = vf.Barrel(volume, with_unit=with_unit).bbl_to(to_unit)
    elif from_unit in {"m3", "m³"}:
        result = vf.CubicMeter(volume, with_unit=with_unit).m3_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")

    return round_number(result) if rounded_result else result
