"""
This module provides a function to calculate density based on mass and volume, 
and convert it to various units of density.

Function:
    - density_calculator: A function that calculates density from mass and volume, 
      and converts it to the specified unit. The density can be returned either as a 
      numeric value or as a string with the unit included.

Units Supported for Conversion:
    - 'g/cm³': Gram per cubic centimeter, a unit of density.
    - 'lb/ft³': Pound per cubic foot, a unit of density in the imperial system.
    - 'oz/in³': Ounce per cubic inch, a unit of density in the imperial system.
    - 'kg/m³': Kilogram per cubic meter, a unit of density.

Parameters:
    - mass (float): The mass in kilograms (kg).
    - volume (float): The volume in cubic meters (m³).
    - density_unit (str): The desired unit for the resulting density. Supported units are:
      'g/cm³', 'lb/ft³', 'oz/in³', 'kg/m³'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, 
      which returns just the numeric value.

Returns:
    - Union[float, str]: The calculated density in the specified unit. The result is returned as a float 
      if `with_unit` is False, or as a string with the unit if `with_unit` is True.

Raises:
    - ValueError: If the specified density unit is not recognized.

Usage Example:
    # Calculate the density from 10 kg and 2 m³, and convert it to g/cm³
    result = density_calculator(10, 2, 'g/cm³')
    print(result)  # Output: 5.0

    # Calculate the density from 10 kg and 2 m³, and include the unit in the result
    result = density_calculator(10, 2, 'g/cm³', True)
    print(result)  # Output: "5.0 g/cm³"

    # Handle an unknown unit (will raise a ValueError)
    result = density_calculator(10, 2, 'unknown_unit')
    # Raises ValueError: Unknown unit: unknown_unit
"""

from typing import Union


def density_calculator(
    mass: float, volume: float, density_unit: str, with_unit: bool = False
) -> Union[float, str]:
    result = mass / volume

    if density_unit == "kg/m³" or density_unit == "kg/m3":
        return f"{result} kg/m³" if with_unit else result

    units = {
        "g/cm³": result / 1000,
        "g/cm3": result / 1000,
        "lb/ft³": result * 0.062428,
        "lb/ft3": result * 0.062428,
        "oz/in³": result * 0.0005780367,
        "oz/in3": result * 0.0005780367,
    }

    if density_unit in units:
        return (
            f"{units[density_unit]} {density_unit}"
            if with_unit
            else units[density_unit]
        )

    raise ValueError(f"Unknown unit: {density_unit}")
