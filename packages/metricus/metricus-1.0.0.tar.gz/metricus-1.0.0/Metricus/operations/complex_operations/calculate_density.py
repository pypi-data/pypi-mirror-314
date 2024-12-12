"""
This module provides a function to calculate the density based on mass, volume, and the desired units for both.

Function:
    - calculate_density: A function that calculates the density by converting the provided mass and volume 
      into the correct units and then calculating the resulting density in the specified unit.

Units Supported for Conversion:
    - Mass Units:
        - 'kilogram': Kilogram, the base unit of mass in the metric system.
        - Other mass units can be converted to kilogram using the `mass_converter` function from the `operations.mass` module.
    
    - Volume Units:
        - 'cubic_meter': Cubic Meter (m³), the standard unit for volume.
        - Other volume units can be converted to cubic meter using the `volume_converter` function from the `operations.volume` module.
    
    - Density Units:
        - 'kg/m³': Kilogram per cubic meter (kg/m³), the standard unit of density in the metric system.
        - 'g/cm³': Gram per cubic centimeter (g/cm³), a unit of density.
        - 'lb/ft³': Pound per cubic foot (lb/ft³), a unit of density in the imperial system.
        - 'oz/in³': Ounce per cubic inch (oz/in³), a unit of density in the imperial system.

Parameters:
    - mass (float): The mass value to be used in the density calculation.
    - volume (float): The volume value to be used in the density calculation.
    - density_unit (str, optional): The unit of density to return. Defaults to 'kg/m³'. Supported units include:
      'kg/m³', 'g/cm³', 'lb/ft³', 'oz/in³'.
    - mass_unit (str, optional): The unit of mass for the provided mass value. Defaults to 'kilogram'. 
      Other units are converted to kilograms.
    - volume_unit (str, optional): The unit of volume for the provided volume value. Defaults to 'cubic_meter'. 
      Other units are converted to cubic meters.
    - rounded_result (bool, optional): If True, the result is rounded. Defaults to False.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, which returns just the numeric value.

Returns:
    - Union[float, str]: The calculated density in the specified unit. The result is returned as a float if `with_unit` is False, 
      or as a string with the unit if `with_unit` is True.

Raises:
    - ValueError: If the specified density unit, mass unit, or volume unit is not recognized.

Usage Example:
    # Calculate the density from 10 kilograms and 2 cubic meters, converting units to g/cm³
    result = calculate_density(10, 2, density_unit='g/cm³', mass_unit='kilogram', volume_unit='cubic_meter')
    print(result)  # Output: 0.005

    # Calculate the density from 10 kilograms and 2 cubic meters, with the result including the unit
    result = calculate_density(10, 2, density_unit='g/cm³', mass_unit='kilogram', volume_unit='cubic_meter', with_unit=True)
    print(result)  # Output: "0.005 g/cm³"

    # Calculate the density from 10 pounds and 2 cubic feet, with the result including the unit
    result = calculate_density(10, 2, density_unit='lb/ft³', mass_unit='pound', volume_unit='cubic_foot', with_unit=True)
    print(result)  # Output: "5.0 lb/ft³"
"""

from typing import Union

from Metricus._formulas.complex_formulas import density_calculator
from Metricus.operations import mass as m
from Metricus.operations import volume as v
from Metricus.utilities import round_number

dec = density_calculator.density_calculator


def calculate_density(
    mass: float,
    volume: float,
    density_unit: str = "kg/m³",
    mass_unit: str = "kilogram",
    volume_unit: str = "m3",
    rounded_result: bool = False,
    with_unit: bool = False,
) -> Union[float, str]:
    """
    Calculate the density based on mass and volume values, converting the units if necessary.

    This function calculates the density using the formula `Density = Mass / Volume`. It also handles unit conversions
    for mass, volume, and density. The result can be rounded based on the `rounded_result` parameter.

    Parameters:
    - mass (float): The mass value to be used in the density calculation.
    - volume (float): The volume value to be used in the density calculation.
    - density_unit (str): The unit in which the density should be returned. Default is 'kg/m³'.
    - mass_unit (str): The unit of the provided mass. Default is 'kilogram'.
    - volume_unit (str): The unit of the provided volume. Default is 'cubic_meter'.
    - rounded_result (bool): If True, the result will be rounded. Default is False.
    - with_unit (bool): Whether to include the unit in the result. Default is False, which returns only the numeric value.

    Returns:
    - Union[float, str]: The calculated density, either as a float (if `with_unit` is False) or a string
      including the unit (if `with_unit` is True).

    Example:
    >>> calculate_density(10, 2)
    5.0
    >>> calculate_density(10, 2, density_unit='g/cm³', with_unit=True)
    '0.005 g/cm³'
    """

    # Convert mass to kilogram if necessary
    kilogram = (
        m.mass_converter(mass, mass_unit, "kilogram")
        if mass_unit != "kilogram"
        else mass
    )

    # Convert volume to cubic meter if necessary
    cubic_meter = (
        v.volume_converter(volume, volume_unit, "m3")
        if volume_unit != "m3" and volume_unit != "m³"
        else volume
    )

    result = dec(kilogram, cubic_meter, density_unit=density_unit, with_unit=with_unit)

    return round_number(result) if rounded_result else result
