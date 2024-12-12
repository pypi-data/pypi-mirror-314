"""
This module provides classes for converting pressure between different units.

Classes:

    - PressureUnit: A base class for pressure conversions. It handles the pressure value and whether or not the unit should be included in the output.
    - Pascal: A class for converting pressure from pascals (Pa) to other units such as millimeters of mercury (mmHg), pounds per square inch (psi), bars (bar), and atmospheres (atm).
    - MillimeterOfMercury: A class for converting pressure from millimeters of mercury (mmHg) to other units such as pascals (Pa), pounds per square inch (psi), bars (bar), and atmospheres (atm).
    - PoundForcePerSquareInch: A class for converting pressure from pounds per square inch (psi) to other units such as pascals (Pa), millimeters of mercury (mmHg), bars (bar), and atmospheres (atm).
    - Bar: A class for converting pressure from bars (bar) to other units such as pascals (Pa), millimeters of mercury (mmHg), pounds per square inch (psi), and atmospheres (atm).
    - Atmosphere: A class for converting pressure from atmospheres (atm) to other units such as pascals (Pa), millimeters of mercury (mmHg), pounds per square inch (psi), and bars (bar).

Usage Example:

    # Create a Pascal object
    pressure_pa = Pascal(101325, with_unit=True)

    # Convert 101325 pascals to atmospheres
    result = pressure_pa.pascal_to('atmosphere')
    print(result)  # Output: "1.0 atm"

    # Create a MillimeterOfMercury object
    pressure_mmHg = MillimeterOfMercury(760, with_unit=True)

    # Convert 760 mmHg to pascals
    result = pressure_mmHg.mmHg_to('pascal')
    print(result)  # Output: "101325 Pa"

    # Create a PoundForcePerSquareInch object
    pressure_psi = PoundForcePerSquareInch(14.6959, with_unit=True)

    # Convert 14.6959 psi to atmospheres
    result = pressure_psi.psi_to('atmosphere')
    print(result)  # Output: "1.0 atm"

    # Create a Bar object
    pressure_bar = Bar(1, with_unit=True)

    # Convert 1 bar to pascals
    result = pressure_bar.bar_to('pascal')
    print(result)  # Output: "100000 Pa"

    # Create an Atmosphere object
    pressure_atm = Atmosphere(1, with_unit=True)

    # Convert 1 atmosphere to psi
    result = pressure_atm.atmosphere_to('psi')
    print(result)  # Output: "14.6959 psi"
"""

from typing import Union


# Base class for Pressure Units
class PressureUnit:
    """
    A base class for representing and converting pressure units.

    Attributes:
    -----------
    num : float
        The numerical value of the pressure unit.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `PressureUnit` instance with a numerical value and an optional flag for including units in the result.
    format_result(self, result: float, unit: str) -> Union[float, str]
        Formats the result to include the appropriate unit if `with_unit` is set to `True`.
    """

    def __init__(self, num: float, with_unit: bool = False) -> None:
        self.num = num
        self.with_unit = with_unit

    def format_result(self, result: float, unit: str) -> Union[float, str]:
        """
        Formats the result to include the appropriate unit if `with_unit` is set to `True`.

        Parameters:
        -----------
        result : float
            The numerical result of the pressure conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        units_map = {
            "pascal": "Pa",
            "mmHg": "mmHg",
            "psi": "psi",
            "bar": "bar",
            "atmosphere": "atm",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Pascal
class Pascal(PressureUnit):
    """
    A class for converting pressure from pascals to other units.

    Methods:
    --------
    pascal_to(self, unit: str) -> Union[float, str]
        Converts the pressure from pascals to the specified unit.
    """

    def pascal_to(self, unit: str) -> Union[float, str]:
        """
        Converts the pressure from pascals to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'mmHg', 'psi', 'bar', and 'atmosphere'.

        Returns:
        --------
        Union[float, str]
            The converted pressure value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "mmHg":
            result = self.num / 133.322
        elif unit == "psi":
            result = self.num / 6894.76
        elif unit == "bar":
            result = self.num / 100000
        elif unit == "atmosphere":
            result = self.num / 101325
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Millimeter of Mercury
class MillimeterOfMercury(PressureUnit):
    """
    A class for converting pressure from millimeters of mercury (mmHg) to other units.

    Methods:
    --------
    mmHg_to(self, unit: str) -> Union[float, str]
        Converts the pressure from millimeters of mercury to the specified unit.
    """

    def mmHg_to(self, unit: str) -> Union[float, str]:
        """
        Converts the pressure from millimeters of mercury to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'pascal', 'psi', 'bar', and 'atmosphere'.

        Returns:
        --------
        Union[float, str]
            The converted pressure value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "pascal":
            result = self.num * 133.322
        elif unit == "psi":
            result = (self.num * 133.322) / 6894.76
        elif unit == "bar":
            result = (self.num * 133.322) / 100000
        elif unit == "atmosphere":
            result = self.num / 760
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Pound-force per Square Inch
class PoundForcePerSquareInch(PressureUnit):
    """
    A class for converting pressure from pound-force per square inch (psi) to other units.

    Methods:
    --------
    psi_to(self, unit: str) -> Union[float, str]
        Converts the pressure from pound-force per square inch to the specified unit.
    """

    def psi_to(self, unit: str) -> Union[float, str]:
        """
        Converts the pressure from pound-force per square inch to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'pascal', 'mmHg', 'bar', and 'atmosphere'.

        Returns:
        --------
        Union[float, str]
            The converted pressure value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "pascal":
            result = self.num * 6894.76
        elif unit == "mmHg":
            result = (self.num * 6894.76) / 133.322
        elif unit == "bar":
            result = (self.num * 6894.76) / 100000
        elif unit == "atmosphere":
            result = self.num / 14.6959
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Bar
class Bar(PressureUnit):
    """
    A class for converting pressure from bars to other units.

    Methods:
    --------
    bar_to(self, unit: str) -> Union[float, str]
        Converts the pressure from bars to the specified unit.
    """

    def bar_to(self, unit: str) -> Union[float, str]:
        """
        Converts the pressure from bars to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'pascal', 'mmHg', 'psi', and 'atmosphere'.

        Returns:
        --------
        Union[float, str]
            The converted pressure value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "pascal":
            result = self.num * 100000
        elif unit == "mmHg":
            result = (self.num * 100000) / 133.322
        elif unit == "psi":
            result = (self.num * 100000) / 6894.76
        elif unit == "atmosphere":
            result = self.num / 1.01325
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Atmosphere
class Atmosphere(PressureUnit):
    """
    A class for converting pressure from atmospheres to other units.

    Methods:
    --------
    atmosphere_to(self, unit: str) -> Union[float, str]
        Converts the pressure from atmospheres to the specified unit.
    """

    def atmosphere_to(self, unit: str) -> Union[float, str]:
        """
        Converts the pressure from atmospheres to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'pascal', 'mmHg', 'psi', and 'bar'.

        Returns:
        --------
        Union[float, str]
            The converted pressure value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "pascal":
            result = self.num * 101325
        elif unit == "mmHg":
            result = self.num * 760
        elif unit == "psi":
            result = self.num * 14.6959
        elif unit == "bar":
            result = self.num * 1.01325
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)
