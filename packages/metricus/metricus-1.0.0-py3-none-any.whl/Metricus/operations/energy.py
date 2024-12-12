"""
This script provides a function to convert energy between different units of measurement.

The energy_converter function accepts an energy value and converts it from one unit to another using predefined conversion formulas. 
It supports a variety of energy units, including electronvolts, calories, joules, British thermal units (BTU), kilocalories, and kilowatt-hours. 
The conversion is performed by leveraging the energy_formulas module, which contains specific methods for handling each energy unit.

### Supported Units:
- "electronvolt" (eV)
- "calorie" (cal)
- "joule" (J)
- "british_thermal_unit" (BTU)
- "kilocalorie" (kcal)
- "kilowatt_hour" (kWh)

### Main Function:
- energy_converter(energy: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]

  Converts the input energy (energy) from a given unit (from_unit) to a target unit (to_unit). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. The with_unit parameter allows for an optional
  string output that includes the unit in the result. If humanized_input is set to True, the input units can be written in a more 
  user-friendly format (e.g., "BTU" instead of "btu").

### Example Usage:
- Converting 10 electronvolts (eV) to joules (J):
    
python
    energy_converter(10, "electronvolt", "joule")

- Converting 10 electronvolts (eV) to joules (J) with the unit in the result:
    
python
    energy_converter(10, "electronvolt", "joule", with_unit=True)

- Converting with humanized input:
    
python
    energy_converter(10, "british thermal unit", "joule", humanized_input=True)

### Error Handling:
- If either from_unit or to_unit is not recognized (i.e., not in the supported unit_list), the function raises a ValueError.

Dependencies:
- The script uses the energy_formulas module from the formulas package to perform the actual conversion operations.

"""

from typing import Union

from Metricus._formulas import energy_formulas as ef
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "electronvolt",
    "calorie",
    "joule",
    "btu",
    "kilocalorie",
    "kilowatt_hour",
]


def energy_converter(
    energy: float, from_unit: str, to_unit: str, rounded_result: bool = False, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given energy value from one unit to another.

    Args:
        energy (float): The energy value to be converted.
        from_unit (str): The unit of the energy value to convert from.
        to_unit (str): The unit to convert the energy value to.
        rounded_result (bool, optional): If True, the result will be rounded to the nearest integer. Defaults to False.
        humanized_input (bool, optional): If True, the input units are processed with a human-friendly format (e.g., "BTU"). Defaults to False.
        with_unit (bool, optional): If True, the result will include the unit of measurement. Defaults to False.

    Returns:
        Union[float, str]: The converted energy value. If with_unit is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted energy.

    Raises:
        ValueError: If either from_unit or to_unit is not recognized (not in unit_list).

    The function uses the energy_formulas module from the formulas package to handle the actual conversions.
    The conversion process is determined based on the from_unit and to_unit parameters.

    Example usage:
        energy_converter(10, "electronvolt", "joule")  # Converts 10 electronvolts to joules
        energy_converter(10, "electronvolt", "joule", with_unit=True)  # Converts 10 electronvolts to joules and includes the unit in the result
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("Unknown unit of measurement")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(energy) if rounded_result else energy
    elif from_unit == "electronvolt":
        result = ef.Electronvolt(energy, with_unit=with_unit).electronvolt_to(to_unit)
    elif from_unit == "calorie":
        result = ef.Calorie(energy, with_unit=with_unit).calorie_to(to_unit)
    elif from_unit == "joule":
        result = ef.Joule(energy, with_unit=with_unit).joule_to(to_unit)
    elif from_unit == "btu":
        result = ef.BritishThermalUnit(
            energy, with_unit=with_unit
        ).btu_to(to_unit)
    elif from_unit == "kilocalorie":
        result = ef.Kilocalorie(energy, with_unit=with_unit).kilocalorie_to(to_unit)
    elif from_unit == "kilowatt_hour":
        result = ef.KilowattHour(energy, with_unit=with_unit).kilowatt_hour_to(to_unit)
    else:
        raise ValueError("Unknown unit of measurement")
    
    return round_number(result) if rounded_result else result
