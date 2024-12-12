"""
This module provides a function to calculate force based on mass and acceleration, 
and convert it to various units of force.

Function:
    - force_calculator: A function that calculates force from mass and acceleration, 
      and converts it to the specified unit. The force can be returned either as a 
      numeric value or as a string with the unit included.

Units Supported for Conversion:
    - 'dyne': Dyne, a CGS unit of force.
    - 'kilonewton': Kilonewton, a metric unit of force.
    - 'pound_force': Pound-force, a unit of force in the imperial system.
    - 'ounce_force': Ounce-force, a unit of force in the imperial system.
    - 'ton_force': Ton-force, a unit of force in the imperial system.
    - 'kilogram_force': Kilogram-force, a unit of force based on the mass of one kilogram.
    - 'gram_force': Gram-force, a unit of force based on the mass of one gram.
    - 'millinewton': Millinewton, a metric unit of force equal to one-thousandth of a newton.
    - 'poundal': Poundal, a unit of force in the imperial system.
    - 'slug_force': Slug-force, a unit of force in the imperial system based on the mass of a slug.

Parameters:
    - kg (float): The mass in kilograms (kg).
    - meter_per_second_squared (float): The acceleration in meters per second squared (m/s²).
    - force_unit (str): The desired unit for the resulting force. Supported units are:
      'dyne', 'kilonewton', 'pound_force', 'ounce_force', 'ton_force', 'kilogram_force', 
      'gram_force', 'millinewton', 'poundal', 'slug_force'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, 
      which returns just the numeric value.

Returns:
    - Union[float, str]: The calculated force in the specified unit. The result is returned as a float 
      if `with_unit` is False, or as a string with the unit if `with_unit` is True.

Raises:
    - ValueError: If the specified force unit is not recognized.

Usage Example:
    # Calculate the force from 10 kg and 9.81 m/s², and convert it to kilonewton
    result = force_calculator(10, 9.81, 'kilonewton')
    print(result)  # Output: 0.0981

    # Calculate the force from 10 kg and 9.81 m/s², and include the unit in the result
    result = force_calculator(10, 9.81, 'kilonewton', True)
    print(result)  # Output: "0.0981 kN"

    # Handle an unknown unit (will raise a ValueError)
    result = force_calculator(10, 9.81, 'unknown_unit')
    # Raises ValueError: The measurement has an unknown unit: unknown_unit
"""

from typing import Union

from Metricus._formulas import force_formulas as ff


def force_calculator(
    kg: float, meter_per_second_squared: float, force_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Calculate the force based on the given mass and acceleration, and convert it to the specified unit.

    Parameters:
    - kg (float): The mass in kilograms (kg).
    - meter_per_second_squared (float): The acceleration in meters per second squared (m/s²).
    - force_unit (str): The desired unit for the resulting force. Supported units are:
        'dyne', 'kilonewton', 'pound_force', 'ounce_force', 'ton_force', 'kilogram_force',
        'gram_force', 'millinewton', 'poundal', 'slug_force'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, which returns just the numeric value.

    Returns:
    - Union[float, str]: The calculated force in the specified unit. The result is returned as a float if `with_unit` is False,
      or as a string with the unit if `with_unit` is True.

    Raises:
    - ValueError: If the specified force unit is not recognized.

    Example:
    >>> force_calculator(10, 9.81, 'kilonewton')
    0.0981

    >>> force_calculator(10, 9.81, 'kilonewton', True)
    '0.0981 kN'

    >>> force_calculator(10, 9.81, 'unknown_unit')
    ValueError: The measurement has an unknown unit: unknown_unit
    """
    # Result in Newton
    result = kg * meter_per_second_squared

    if force_unit == "newton":
        return f"{result} N" if with_unit else result

    units = [
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

    if force_unit in units:
        return getattr(ff.Newton(result, with_unit=with_unit), "newton_to")(force_unit)

    raise ValueError(f"The measurement has an unknown unit: {force_unit}")
