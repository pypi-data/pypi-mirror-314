"""
This module provides classes for converting acceleration between different units.

Classes:
    - Acceleration: A base class for acceleration conversions. It handles the acceleration value and whether or not the unit should be included in the output.
    - MeterPerSecondSquared: A class for converting acceleration from Meter per Second Squared (m/s²) to other units such as Foot per Second Squared (ft/s²), Centimeter per Second Squared (cm/s²), Gal (Gal), Inch per Second Squared (in/s²), Kilometer per Hour Squared (km/h²), Mile per Hour Squared (mi/h²), and Gravity (g).
    - FootPerSecondSquared: A class for converting acceleration from Foot per Second Squared (ft/s²) to other units such as Meter per Second Squared (m/s²), Centimeter per Second Squared (cm/s²), Gal (Gal), Inch per Second Squared (in/s²), Kilometer per Hour Squared (km/h²), Mile per Hour Squared (mi/h²), and Gravity (g).
    - CentimeterPerSecondSquared: A class for converting acceleration from Centimeter per Second Squared (cm/s²) to other units such as Meter per Second Squared (m/s²), Foot per Second Squared (ft/s²), Gal (Gal), Inch per Second Squared (in/s²), Kilometer per Hour Squared (km/h²), Mile per Hour Squared (mi/h²), and Gravity (g).
    - Gal: A class for converting acceleration from Gal (Gal) to other units such as Meter per Second Squared (m/s²), Foot per Second Squared (ft/s²), Centimeter per Second Squared (cm/s²), Inch per Second Squared (in/s²), Kilometer per Hour Squared (km/h²), Mile per Hour Squared (mi/h²), and Gravity (g).
    - InchPerSecondSquared: A class for converting acceleration from Inch per Second Squared (in/s²) to other units such as Meter per Second Squared (m/s²), Foot per Second Squared (ft/s²), Centimeter per Second Squared (cm/s²), Gal (Gal), Kilometer per Hour Squared (km/h²), Mile per Hour Squared (mi/h²), and Gravity (g).
    - KilometerPerHourSquared: A class for converting acceleration from Kilometer per Hour Squared (km/h²) to other units such as Meter per Second Squared (m/s²), Foot per Second Squared (ft/s²), Centimeter per Second Squared (cm/s²), Gal (Gal), Inch per Second Squared (in/s²), Mile per Hour Squared (mi/h²), and Gravity (g).
    - MilePerHourSquared: A class for converting acceleration from Mile per Hour Squared (mi/h²) to other units such as Meter per Second Squared (m/s²), Foot per Second Squared (ft/s²), Centimeter per Second Squared (cm/s²), Gal (Gal), Inch per Second Squared (in/s²), Kilometer per Hour Squared (km/h²), and Gravity (g).
    - Gravity: A class for converting acceleration from Gravity (g) to other units such as Meter per Second Squared (m/s²), Foot per Second Squared (ft/s²), Centimeter per Second Squared (cm/s²), Gal (Gal), Inch per Second Squared (in/s²), Kilometer per Hour Squared (km/h²), and Mile per Hour Squared (mi/h²).

Usage Example:
    # Create a MeterPerSecondSquared object
    acc_mps2 = MeterPerSecondSquared(9.81, with_unit=True)
    # Convert 9.81 m/s² to foot per second squared
    result = acc_mps2.mps2_to('foot_per_second_squared')
    print(result)  # Output: "32.174 ft/s²"

    # Create a FootPerSecondSquared object
    acc_fps2 = FootPerSecondSquared(32.174, with_unit=False)
    # Convert 32.174 ft/s² to meter per second squared
    result = acc_fps2.fps2_to('meter_per_second_squared')
    print(result)  # Output: 9.81

    # Create a Gal object
    acc_gal = Gal(980.665, with_unit=True)
    # Convert 980.665 Gal to meter per second squared
    result = acc_gal.gal_to('meter_per_second_squared')
    print(result)  # Output: "9.81 m/s²"

    # Create a KilometerPerHourSquared object
    acc_kmh2 = KilometerPerHourSquared(12960, with_unit=True)
    # Convert 12960 km/h² to meter per second squared
    result = acc_kmh2.kmh2_to('meter_per_second_squared')
    print(result)  # Output: "1.0 m/s²"
"""

from typing import Union


# Base class for acceleration units
class Acceleration:
    """
    A base class for representing and converting accelerations.

    Attributes:
    -----------
    num : float
        The numerical value of the acceleration.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `Acceleration` instance with a numerical value and an optional flag for including units in the result.
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
            The numerical result of the acceleration conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        units_map = {
            "meter_per_second_squared": "m/s²",
            "foot_per_second_squared": "ft/s²",
            "centimeter_per_second_squared": "cm/s²",
            "gal": "Gal",
            "inch_per_second_squared": "in/s²",
            "kilometer_per_hour_squared": "km/h²",
            "mile_per_hour_squared": "mi/h²",
            "gravity": "g",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Meter Per Second Squared
class MeterPerSecondSquared(Acceleration):
    """
    A class for converting acceleration from Meter per Second Squared (m/s²) to other units.

    Methods:
    --------
    mps2_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Meter per Second Squared to the specified unit.
    """

    def mps2_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Meter per Second Squared to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'foot_per_second_squared', 'centimeter_per_second_squared',
            'gal', 'inch_per_second_squared', 'kilometer_per_hour_squared', 'mile_per_hour_squared', and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "foot_per_second_squared":
            result = self.num * 3.28084
        elif unit == "centimeter_per_second_squared":
            result = self.num * 100
        elif unit == "gal":
            result = self.num * 1000
        elif unit == "inch_per_second_squared":
            result = self.num * 39.3701
        elif unit == "kilometer_per_hour_squared":
            result = self.num * 12960
        elif unit == "mile_per_hour_squared":
            result = self.num * 8047.16
        elif unit == "gravity":
            result = self.num / 9.81
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Foot Per Second Squared
class FootPerSecondSquared(Acceleration):
    """
    A class for converting acceleration from Foot per Second Squared (ft/s²) to other units.

    Methods:
    --------
    fps2_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Foot per Second Squared to the specified unit.
    """

    def fps2_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Foot per Second Squared to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'centimeter_per_second_squared',
            'gal', 'inch_per_second_squared', 'kilometer_per_hour_squared', 'mile_per_hour_squared', and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num / 3.28084
        elif unit == "centimeter_per_second_squared":
            result = self.num * 30.48
        elif unit == "gal":
            result = self.num * 304.8
        elif unit == "inch_per_second_squared":
            result = self.num * 12
        elif unit == "kilometer_per_hour_squared":
            result = self.num * 3960
        elif unit == "mile_per_hour_squared":
            result = self.num * 2414.52
        elif unit == "gravity":
            result = self.num / 32.174
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Centimeter Per Second Squared
class CentimeterPerSecondSquared(Acceleration):
    """
    A class for converting acceleration from Centimeter per Second Squared (cm/s²) to other units.

    Methods:
    --------
    cmps2_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Centimeter per Second Squared to the specified unit.
    """

    def cmps2_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Centimeter per Second Squared to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'foot_per_second_squared',
            'gal', 'inch_per_second_squared', 'kilometer_per_hour_squared', 'mile_per_hour_squared', and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num / 100
        elif unit == "foot_per_second_squared":
            result = self.num / 30.48
        elif unit == "gal":
            result = self.num * 10
        elif unit == "inch_per_second_squared":
            result = self.num / 2.54
        elif unit == "kilometer_per_hour_squared":
            result = self.num * 129.6
        elif unit == "mile_per_hour_squared":
            result = self.num * 80.471
        elif unit == "gravity":
            result = self.num / 981
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Gal
class Gal(Acceleration):
    """
    A class for converting acceleration from Gal (Galileo) to other units.

    Methods:
    --------
    gal_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Gal to the specified unit.
    """

    def gal_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Gal (Galileo) to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'foot_per_second_squared',
            'centimeter_per_second_squared', 'inch_per_second_squared', 'kilometer_per_hour_squared',
            'mile_per_hour_squared', and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num / 1000
        elif unit == "foot_per_second_squared":
            result = self.num / 304.8
        elif unit == "centimeter_per_second_squared":
            result = self.num * 10
        elif unit == "inch_per_second_squared":
            result = self.num / 25.4
        elif unit == "kilometer_per_hour_squared":
            result = self.num / 8.64
        elif unit == "mile_per_hour_squared":
            result = self.num / 13.712
        elif unit == "gravity":
            result = self.num / 980.665
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Inch Per Second Squared
class InchPerSecondSquared(Acceleration):
    """
    A class for converting acceleration from Inch per Second Squared (in/s²) to other units.

    Methods:
    --------
    ips2_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Inch per Second Squared to the specified unit.
    """

    def ips2_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Inch per Second Squared to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'foot_per_second_squared',
            'centimeter_per_second_squared', 'gal', 'kilometer_per_hour_squared', 'mile_per_hour_squared',
            and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num / 39.3701
        elif unit == "foot_per_second_squared":
            result = self.num / 12
        elif unit == "centimeter_per_second_squared":
            result = self.num * 2.54
        elif unit == "gal":
            result = self.num * 25.4
        elif unit == "kilometer_per_hour_squared":
            result = self.num * 330
        elif unit == "mile_per_hour_squared":
            result = self.num * 206.868
        elif unit == "gravity":
            result = self.num / 386.102
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Kilometer Per Hour Squared
class KilometerPerHourSquared(Acceleration):
    """
    A class for converting acceleration from Kilometer per Hour Squared (km/h²) to other units.

    Methods:
    --------
    kmh2_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Kilometer per Hour Squared to the specified unit.
    """

    def kmh2_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Kilometer per Hour Squared to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'foot_per_second_squared',
            'centimeter_per_second_squared', 'gal', 'inch_per_second_squared', 'mile_per_hour_squared', and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num / 12960
        elif unit == "foot_per_second_squared":
            result = self.num / 3960
        elif unit == "centimeter_per_second_squared":
            result = self.num / 129.6
        elif unit == "gal":
            result = self.num * 8.64
        elif unit == "inch_per_second_squared":
            result = self.num / 330
        elif unit == "mile_per_hour_squared":
            result = self.num * 0.621371
        elif unit == "gravity":
            result = self.num / 9485.9
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Mile Per Hour Squared
class MilePerHourSquared(Acceleration):
    """
    A class for converting acceleration from Mile per Hour Squared (mi/h²) to other units.

    Methods:
    --------
    mph2_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Mile per Hour Squared to the specified unit.
    """

    def mph2_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Mile per Hour Squared to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'foot_per_second_squared',
            'centimeter_per_second_squared', 'gal', 'inch_per_second_squared', 'kilometer_per_hour_squared',
            and 'gravity'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num / 8047.16
        elif unit == "foot_per_second_squared":
            result = self.num / 2414.52
        elif unit == "centimeter_per_second_squared":
            result = self.num / 80.471
        elif unit == "gal":
            result = self.num * 13.712
        elif unit == "inch_per_second_squared":
            result = self.num / 206.868
        elif unit == "kilometer_per_hour_squared":
            result = self.num / 0.621371
        elif unit == "gravity":
            result = self.num / 6246.9
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Gravity
class Gravity(Acceleration):
    """
    A class for converting acceleration from Gravity (g) to other units.

    Methods:
    --------
    g_to(self, unit: str) -> Union[float, str]
        Converts acceleration from Gravity to the specified unit.
    """

    def g_to(self, unit: str) -> Union[float, str]:
        """
        Converts acceleration from Gravity (g) to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'meter_per_second_squared', 'foot_per_second_squared',
            'centimeter_per_second_squared', 'gal', 'inch_per_second_squared', 'kilometer_per_hour_squared',
            and 'mile_per_hour_squared'.

        Returns:
        --------
        Union[float, str]
            The converted acceleration value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "meter_per_second_squared":
            result = self.num * 9.81
        elif unit == "foot_per_second_squared":
            result = self.num * 32.174
        elif unit == "centimeter_per_second_squared":
            result = self.num * 981
        elif unit == "gal":
            result = self.num * 980.665
        elif unit == "inch_per_second_squared":
            result = self.num * 386.102
        elif unit == "kilometer_per_hour_squared":
            result = self.num * 9485.9
        elif unit == "mile_per_hour_squared":
            result = self.num * 6246.9
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)
