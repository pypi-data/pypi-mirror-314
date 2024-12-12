"""
This module provides classes for converting speeds between different units.

Classes:

    - Speed: A base class for speed conversions. It handles the speed value and whether or not the unit should be included in the output.
    - MetersPerSecond: A class for converting speeds from meters per second (m/s) to other units such as kilometers per hour (km/h), miles per hour (mph), and knots (kn).
    - KilometersPerHour: A class for converting speeds from kilometers per hour (km/h) to other units such as meters per second (m/s), miles per hour (mph), and knots (kn).
    - MilesPerHour: A class for converting speeds from miles per hour (mph) to other units such as meters per second (m/s), kilometers per hour (km/h), and knots (kn).
    - Knots: A class for converting speeds from knots (kn) to other units such as meters per second (m/s), kilometers per hour (km/h), and miles per hour (mph).

Usage Example:

    # Create a MetersPerSecond object
    speed = MetersPerSecond(10, with_unit=True)

    # Convert 10 meters per second to kilometers per hour
    result = speed.mps_to('km/h')
    print(result)  # Output: "36.0 km/h"
    
    # Create a KilometersPerHour object
    speed = KilometersPerHour(36, with_unit=True)

    # Convert 36 km/h to miles per hour
    result = speed.kmph_to('mph')
    print(result)  # Output: "22.36936357528714 mph"

    # Create a MilesPerHour object
    speed = MilesPerHour(22, with_unit=False)

    # Convert 22 mph to knots
    result = speed.mph_to('kn')
    print(result)  # Output: 19.1159

    # Create a Knots object
    speed = Knots(20, with_unit=True)

    # Convert 20 knots to meters per second
    result = speed.knots_to('m/s')
    print(result)  # Output: "10.288 m/s"
"""

# Speed
from typing import Union


class Speed:
    """
    A class used to represent a speed value and format it with or without the unit abbreviation.

    Attributes
    ----------
    num : float
        The speed value.
    with_unit : bool, optional
        Flag to determine if the unit should be included in the output. Default is False.

    Methods
    -------
    format_result(result: float, unit: str) -> Union[float, str]
        Formats the conversion result by adding the unit if necessary.
    """

    def __init__(self, num: float, with_unit: bool = False) -> None:
        """
        Initializes a Speed object.

        Parameters
        ----------
        num : float
            Speed value.
        with_unit : bool, optional
            Flag to determine if the unit should be included in the output. Default is False.
        """
        self.num = num
        self.with_unit = with_unit

    def format_result(self, result: float, unit: str) -> Union[float, str]:
        """
        Formats the conversion result by adding the unit if necessary.

        Parameters
        ----------
        result : float
            Conversion result.
        unit : str
            Unit to be added to the result.

        Returns
        -------
        Union[float, str]
            Formatted result with or without the unit.
        """
        return f"{result} {unit}" if self.with_unit else result


# MetersPerSecond
class MetersPerSecond(Speed):
    """
    Class to convert speeds from meters per second (m/s) to other speed units.

    Inherits from the Speed base class.
    """

    def mps_to(self, unit: str) -> Union[float, str]:
        """
        Converts speed from meters per second (m/s) to the specified unit.

        :param unit: Unit to which the speed will be converted. It can be 'km/h', 'mph', or 'kn'.
        :type unit: str
        :return: Converted value in the specified unit. If `with_unit` is True, it returns a string with the value and the unit; otherwise, it returns a float.
        :rtype: Union[float, str]
        :raises ValueError: If the specified unit is unrecognized.
        """
        if unit == "km/h":
            result = self.num * 3.6
        elif unit == "mph":
            result = self.num * 2.23694
        elif unit == "kn":
            result = self.num * 1.94384
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# KilometersPerHour
class KilometersPerHour(Speed):
    """
    Class to convert speeds from kilometers per hour (km/h) to other speed units.

    Inherits from the Speed base class.
    """

    def kmph_to(self, unit: str) -> Union[float, str]:
        """
        Converts speed from kilometers per hour (km/h) to the specified unit.

        :param unit: Unit to which the speed will be converted. It can be 'm/s', 'mph', or 'kn'.
        :type unit: str
        :return: Converted value in the specified unit. If `with_unit` is True, it returns a string with the value and the unit; otherwise, it returns a float.
        :rtype: Union[float, str]
        :raises ValueError: If the specified unit is unrecognized.
        """
        if unit == "m/s":
            result = self.num / 3.6
        elif unit == "mph":
            result = self.num / 1.60934
        elif unit == "kn":
            result = self.num / 1.852
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# MilesPerHour
class MilesPerHour(Speed):
    """
    Class to convert speeds from miles per hour (mph) to other speed units.

    Inherits from the Speed base class.
    """

    def mph_to(self, unit: str) -> Union[float, str]:
        """
        Converts speed from miles per hour (mph) to the specified unit.

        :param unit: Unit to which the speed will be converted. It can be 'm/s', 'km/h', or 'kn'.
        :type unit: str
        :return: Converted value in the specified unit. If `with_unit` is True, it returns a string with the value and the unit; otherwise, it returns a float.
        :rtype: Union[float, str]
        :raises ValueError: If the specified unit is unrecognized.
        """
        if unit == "m/s":
            result = self.num / 2.23694
        elif unit == "km/h":
            result = self.num * 1.60934
        elif unit == "kn":
            result = self.num / 1.15078
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Knots
class Knots(Speed):
    """
    Class to convert speeds from knots (kn) to other speed units.

    Inherits from the Speed base class.
    """

    def kn_to(self, unit: str) -> Union[float, str]:
        """
        Converts speed from knots (kn) to the specified unit.

        :param unit: Unit to which the speed will be converted. It can be 'm/s', 'km/h', or 'mph'.
        :type unit: str
        :return: Converted value in the specified unit. If `with_unit` is True, it returns a string with the value and the unit; otherwise, it returns a float.
        :rtype: Union[float, str]
        :raises ValueError: If the specified unit is unrecognized.
        """
        if unit == "m/s":
            result = self.num / 1.94384
        elif unit == "km/h":
            result = self.num * 1.852
        elif unit == "mph":
            result = self.num * 1.15078
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)
