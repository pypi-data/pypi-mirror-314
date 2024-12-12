"""
This module provides a function to calculate pressure based on force and area, 
and convert it to various units of pressure.

Function:
    - pressure_calculator: A function that calculates pressure from force and area, 
      and converts it to the specified unit. The pressure can be returned either as a 
      numeric value or as a string with the unit included.

Units Supported for Conversion:
    - 'pascal': Pascal (Pa), the standard unit of pressure in the metric system (default).
    - 'mmHg': Millimeters of mercury (mmHg), a unit of pressure equal to 1/760 of an atmosphere.
    - 'psi': Pound per square inch (psi), a unit of pressure in the imperial system.
    - 'bar': Bar, a metric unit of pressure.
    - 'atmosphere': Atmosphere (atm), a unit of pressure based on the average atmospheric pressure at sea level.

Parameters:
    - newton (float): The force in newtons (N).
    - square_meter (float): The area in square meters (m²).
    - pressure_unit (str): The desired unit for the resulting pressure. Supported units are:
      'pascal', 'mmHg', 'psi', 'bar', 'atmosphere'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, 
      which returns just the numeric value.

Returns:
    - Union[float, str]: The calculated pressure in the specified unit. The result is returned as a float 
      if `with_unit` is False, or as a string with the unit if `with_unit` is True.

Raises:
    - ValueError: If the specified pressure unit is not recognized.

Usage Example:
    # Calculate the pressure from 100 N and 2 m², and convert it to bar
    result = pressure_calculator(100, 2, 'bar')
    print(result)  # Output: 0.0005

    # Calculate the pressure from 100 N and 2 m², and include the unit in the result
    result = pressure_calculator(100, 2, 'bar', True)
    print(result)  # Output: "0.0005 bar"

    # Handle an unknown unit (will raise a ValueError)
    result = pressure_calculator(100, 2, 'unknown_unit')
    # Raises ValueError: The measurement has an unknown unit: unknown_unit
"""

from typing import Union

from Metricus\._formulas import pressure_formulas as pf


def pressure_calculator(
    newton: float, square_meter: float, pressure_unit: str, with_unit: bool = False
) -> Union[float, str]:
    """
    Calculate the pressure based on the given force and area, and convert it to the specified unit.

    Parameters:
    - newton (float): The force in newtons (N).
    - square_meter (float): The area in square meters (m²).
    - pressure_unit (str): The desired unit for the resulting pressure. Supported units are:
        'bar', 'atm', 'torr', 'psi'.
    - with_unit (bool, optional): If True, returns the result with the unit. Defaults to False, which returns just the numeric value.

    Returns:
    - Union[float, str]: The calculated pressure in the specified unit. The result is returned as a float if `with_unit` is False,
      or as a string with the unit if `with_unit` is True.

    Raises:
    - ValueError: If the specified pressure unit is not recognized.

    Example:
    >>> pressure_calculator(100, 2, 'bar')
    0.0005

    >>> pressure_calculator(100, 2, 'bar', True)
    '0.0005 bar'

    >>> pressure_calculator(100, 2, 'unknown_unit')
    ValueError: The measurement has an unknown unit: unknown_unit
    """
    # Result in Pascal (Pa)
    result = newton / square_meter

    if pressure_unit == "pascal":
        return f"{result} Pa" if with_unit else result

    units = ["pascal", "mmHg", "psi", "bar", "atmosphere"]

    if pressure_unit in units:
        return getattr(pf.Pascal(result, with_unit=with_unit), "pascal_to")(
            pressure_unit
        )

    raise ValueError(f"The measurement has an unknown unit: {pressure_unit}")
