"""
This module provides a function to calculate the pressure based on force, area, and the desired units for both.

Function:
    - calculate_pressure: A function that calculates the pressure by converting the provided force and area 
      into the correct units and then calculating the resulting pressure in the specified unit.

Units Supported for Conversion:
    - Force Units:
        - 'newton': Newton (N), the standard unit of force in the metric system.
        - Other force units can be converted to newton using the `force_converter` function from the `operations.force` module.
    
    - Area Units:
        - 'square_meter': Square Meter (m²), the standard unit for area.
        - Other area units can be converted to square meter using the `area_converter` function from the `operations.area` module.
    
    - Pressure Units:
        - 'pascal': Pascal (Pa), the standard unit of pressure in the metric system.
        - 'bar': Bar, a metric unit of pressure.
        - 'atm': Atmosphere, a unit of pressure based on the average atmospheric pressure at sea level.
        - 'mmHg': mmHg, a unit of pressure equal to 1/760 of an atmosphere.
        - 'psi': Pound per square inch (psi), a unit of pressure in the imperial system.

Parameters:
    - force (float): The force value to be used in the pressure calculation.
    - area (float): The area value to be used in the pressure calculation.
    - pressure_unit (str, optional): The unit of pressure to return. Defaults to 'pascal'. Supported units include:
      'pascal', 'bar', 'atm', 'mmHg', 'psi'.
    - force_unit (str, optional): The unit of force for the provided force value. Defaults to 'newton'. 
      Other units are converted to newtons.
    - area_unit (str, optional): The unit of area for the provided area value. Defaults to 'square_meter'. 
      Other units are converted to square meters.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, which returns just the numeric value.

Returns:
    - Union[float, str]: The calculated pressure in the specified unit. The result is returned as a float if `with_unit` is False, 
      or as a string with the unit if `with_unit` is True.

Raises:
    - ValueError: If the specified pressure unit, force unit, or area unit is not recognized.

Usage Example:
    # Calculate the pressure from 100 poundals and 2 square feet, converting units to pascal
    result = calculate_pressure(100, 2, pressure_unit='pascal', force_unit='poundal, area_unit='square_foot')
    print(result)  # Output: 4788.025

    # Calculate the pressure from 100 pounds and 2 square feet, with the result including the unit
    result = calculate_pressure(100, 2, pressure_unit='bar', force_unit='poundal', area_unit='square_foot', with_unit=True)
    print(result)  # Output: "0.0479 bar"

    # Calculate the pressure from 100 newtons and 2 square meters, with the result including the unit
    result = calculate_pressure(100, 2, pressure_unit='psi', force_unit='newton', area_unit='square_meter', with_unit=True)
    print(result)  # Output: "7.2523 psi"
"""

from typing import Union

from Metricus._formulas.complex_formulas import pressure_calculator
from Metricus.operations import area as a
from Metricus.operations import force as f
from Metricus.utilities import round_number

pf = pressure_calculator.pressure_calculator


def calculate_pressure(
    force: float,
    area: float,
    pressure_unit: str = "pascal",
    force_unit: str = "newton",
    area_unit: str = "square_meter",
    rounded_result: bool = False,
    with_unit: bool = False,
) -> Union[float, str]:
    """
    Calculate the pressure based on force and area values, converting the units if necessary.

    This function calculates the pressure using the formula `Pressure = Force / Area`. It also handles unit conversions
    for force, area, and pressure.

    Parameters:
    - force (float): The force value to be used in the pressure calculation.
    - area (float): The area value to be used in the pressure calculation.
    - pressure_unit (str): The unit in which the pressure should be returned. Default is 'pascal'.
    - force_unit (str): The unit of the provided force. Default is 'newton'.
    - area_unit (str): The unit of the provided area. Default is 'square_meter'.
    - rounded_result (bool): If True, rounds the result to a reasonable number of decimal places. Default is False.
    - with_unit (bool): Whether to include the unit in the result. Default is False, which returns only the numeric value.

    Returns:
    - Union[float, str]: The calculated pressure, either as a float (if `with_unit` is False) or a string
      including the unit (if `with_unit` is True).

    Example:
    >>> calculate_pressure(100, 2)
    50.0
    >>> calculate_pressure(100, 2, pressure_unit='bar', with_unit=True)
    '0.0005 bar'

    Units Supported for Conversion:
    - Force Units:
        - 'newton': Newton (N), the standard unit of force in the metric system.
        - Other force units can be converted to newton using the `force_converter` function from the `operations.force` module.
    
    - Area Units:
        - 'square_meter': Square Meter (m²), the standard unit for area.
        - Other area units can be converted to square meter using the `area_converter` function from the `operations.area` module.
    
    - Pressure Units:
        - 'pascal': Pascal (Pa), the standard unit of pressure in the metric system.
        - 'bar': Bar, a metric unit of pressure.
        - 'atm': Atmosphere, a unit of pressure based on the average atmospheric pressure at sea level.
        - 'mmHg': mmHg, a unit of pressure equal to 1/760 of an atmosphere.
        - 'psi': Pound per square inch (psi), a unit of pressure in the imperial system.

    Raises:
    - ValueError: If the specified pressure unit, force unit, or area unit is not recognized.

    Usage Example:
    # Calculate the pressure from 100 poundals and 2 square feet, converting units to pascal
    result = calculate_pressure(100, 2, pressure_unit='pascal', force_unit='poundal', area_unit='square_foot')
    print(result)  # Output: 4788.025

    # Calculate the pressure from 100 poundals and 2 square feet, with the result including the unit
    result = calculate_pressure(100, 2, pressure_unit='bar', force_unit='poundal', area_unit='square_foot', with_unit=True)
    print(result)  # Output: "0.0479 bar"

    # Calculate the pressure from 100 newtons and 2 square meters, with the result including the unit
    result = calculate_pressure(100, 2, pressure_unit='psi', force_unit='newton', area_unit='square_meter', with_unit=True)
    print(result)  # Output: "7.2523 psi"
    """

    # Convert force to newton if necessary
    newton = (
        f.force_converter(force, force_unit, "newton")
        if force_unit != "newton"
        else force
    )

    # Convert area to square meter if necessary
    square_meter = (
        a.area_converter(area, area_unit, "square_meter")
        if area_unit != "square_meter"
        else area
    )

    # Calculate pressure using the converted values
    result = pf(
        newton=newton,
        square_meter=square_meter,
        pressure_unit=pressure_unit,
        with_unit=with_unit,
    )

    return round_number(result) if rounded_result else result
