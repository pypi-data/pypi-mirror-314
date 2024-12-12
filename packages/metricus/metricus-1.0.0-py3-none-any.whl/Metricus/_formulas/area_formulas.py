"""
This module provides classes for converting areas between different units.

Classes:

    - Area: A base class for area conversions. It handles the area value and whether or not the unit should be included in the output.
    - SquareCentimeter: A class for converting areas from square centimeters (cm²) to other units such as square feet (ft²), square meters (m²), square yards (yd²), acres (ac), hectares (ha), and square kilometers (km²).
    - SquareFoot: A class for converting areas from square feet (ft²) to other units such as square centimeters (cm²), square meters (m²), square yards (yd²), acres (ac), hectares (ha), and square kilometers (km²).
    - SquareYard: A class for converting areas from square yards (yd²) to other units such as square centimeters (cm²), square feet (ft²), square meters (m²), acres (ac), hectares (ha), and square kilometers (km²).
    - SquareMeter: A class for converting areas from square meters (m²) to other units such as square centimeters (cm²), square feet (ft²), square yards (yd²), acres (ac), hectares (ha), and square kilometers (km²).
    - Acre: A class for converting areas from acres (ac) to other units such as square centimeters (cm²), square feet (ft²), square yards (yd²), square meters (m²), hectares (ha), and square kilometers (km²).
    - Hectare: A class for converting areas from hectares (ha) to other units such as square centimeters (cm²), square feet (ft²), square yards (yd²), square meters (m²), acres (ac), and square kilometers (km²).
    - SquareKilometer: A class for converting areas from square kilometers (km²) to other units such as square centimeters (cm²), square feet (ft²), square yards (yd²), square meters (m²), acres (ac), and hectares (ha).

Usage Example:

    # Create a SquareCentimeter object
    area = SquareCentimeter(10000, with_unit=True)

    # Convert 10000 square centimeters to square meters
    result = area.square_centimeter_to('square_meter')
    print(result)  # Output: "1.0 m²"
    
    # Create a SquareFoot object
    area = SquareFoot(100, with_unit=True)

    # Convert 100 square feet to square meters
    result = area.square_foot_to('square_meter')
    print(result)  # Output: "9.2903 m²"

    # Create a SquareYard object
    area = SquareYard(10, with_unit=False)

    # Convert 10 square yards to square meters
    result = area.square_yard_to('square_meter')
    print(result)  # Output: 8.3612736

    # Create a SquareMeter object
    area = SquareMeter(1, with_unit=True)

    # Convert 1 square meter to square feet
    result = area.square_meter_to('square_foot')
    print(result)  # Output: "10.7639 ft²"

    # Create an Acre object
    area = Acre(1, with_unit=True)

    # Convert 1 acre to square meters
    result = area.acre_to('square_meter')
    print(result)  # Output: "4046.86 m²"

    # Create a Hectare object
    area = Hectare(1, with_unit=True)

    # Convert 1 hectare to acres
    result = area.hectare_to('acre')
    print(result)  # Output: "2.47105 ac"

    # Create a SquareKilometer object
    area = SquareKilometer(1, with_unit=True)

    # Convert 1 square kilometer to square meters
    result = area.square_kilometer_to('square_meter')
    print(result)  # Output: "1e6 m²"
"""

from typing import Union


# Base class for Area
class Area:
    """
    A base class for representing and converting areas.

    Attributes:
    -----------
    num : float
        The numerical value of the area.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `Area` instance with a numerical value and an optional flag for including units in the result.
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
            The numerical result of the area conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        units_map = {
            "square_centimeter": "cm²",
            "square_foot": "ft²",
            "square_meter": "m²",
            "square_yard": "yd²",
            "acre": "ac",
            "hectare": "ha",
            "square_kilometer": "km²",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Square Centimeter
class SquareCentimeter(Area):
    """
    A class for converting areas from square centimeters to other units.

    Methods:
    --------
    square_centimeter_to(self, unit: str) -> Union[float, str]
        Converts the area from square centimeters to the specified unit.
    """

    def square_centimeter_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from square centimeters to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_foot', 'square_meter', 'square_yard', 'acre', 'hectare', and 'square_kilometer'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_foot":
            result = self.num / 929.0304
        elif unit == "square_meter":
            result = self.num / 10000
        elif unit == "square_yard":
            result = self.num / 8361.2736
        elif unit == "acre":
            result = self.num / 4.04686e7
        elif unit == "hectare":
            result = self.num / 1e8
        elif unit == "square_kilometer":
            result = self.num / 1e10
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Square Foot
class SquareFoot(Area):
    """
    A class for converting areas from square feet to other units.

    Methods:
    --------
    square_foot_to(self, unit: str) -> Union[float, str]
        Converts the area from square feet to the specified unit.
    """

    def square_foot_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from square feet to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_centimeter', 'square_meter', 'square_yard', 'acre', 'hectare', and 'square_kilometer'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_centimeter":
            result = self.num * 929.0304
        elif unit == "square_meter":
            result = self.num / 10.7639
        elif unit == "square_yard":
            result = self.num / 9
        elif unit == "acre":
            result = self.num / 43560
        elif unit == "hectare":
            result = self.num / 107639
        elif unit == "square_kilometer":
            result = self.num / 1.076e7
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Square Yard
class SquareYard(Area):
    """
    A class for converting areas from square yards to other units.

    Methods:
    --------
    square_yard_to(self, unit: str) -> Union[float, str]
        Converts the area from square yards to the specified unit.
    """

    def square_yard_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from square yards to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_centimeter', 'square_foot', 'square_meter', 'acre', 'hectare', and 'square_kilometer'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_centimeter":
            result = self.num * 8361.2736
        elif unit == "square_foot":
            result = self.num * 9
        elif unit == "square_meter":
            result = self.num / 1.19599
        elif unit == "acre":
            result = self.num / 4840
        elif unit == "hectare":
            result = self.num / 11959.9
        elif unit == "square_kilometer":
            result = self.num / 1.196e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Square Meter
class SquareMeter(Area):
    """
    A class for converting areas from square meters to other units.

    Methods:
    --------
    square_meter_to(self, unit: str) -> Union[float, str]
        Converts the area from square meters to the specified unit.
    """

    def square_meter_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from square meters to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_centimeter', 'square_foot', 'square_yard', 'acre', 'hectare', and 'square_kilometer'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_centimeter":
            result = self.num * 10000
        elif unit == "square_foot":
            result = self.num * 10.7639
        elif unit == "square_yard":
            result = self.num * 1.19599
        elif unit == "acre":
            result = self.num / 4046.86
        elif unit == "hectare":
            result = self.num / 10000
        elif unit == "square_kilometer":
            result = self.num / 1e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Acre
class Acre(Area):
    """
    A class for converting areas from acres to other units.

    Methods:
    --------
    acre_to(self, unit: str) -> Union[float, str]
        Converts the area from acres to the specified unit.
    """

    def acre_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from acres to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_centimeter', 'square_foot', 'square_yard', 'square_meter', 'hectare', and 'square_kilometer'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_centimeter":
            result = self.num * 4.04686e7
        elif unit == "square_foot":
            result = self.num * 43560
        elif unit == "square_yard":
            result = self.num * 4840
        elif unit == "square_meter":
            result = self.num * 4046.86
        elif unit == "hectare":
            result = self.num / 2.47105
        elif unit == "square_kilometer":
            result = self.num / 247.105
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Hectare
class Hectare(Area):
    """
    A class for converting areas from hectares to other units.

    Methods:
    --------
    hectare_to(self, unit: str) -> Union[float, str]
        Converts the area from hectares to the specified unit.
    """

    def hectare_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from hectares to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_centimeter', 'square_foot', 'square_yard', 'square_meter', 'acre', and 'square_kilometer'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_centimeter":
            result = self.num * 1e8
        elif unit == "square_foot":
            result = self.num * 107639
        elif unit == "square_yard":
            result = self.num * 11959.9
        elif unit == "square_meter":
            result = self.num * 10000
        elif unit == "acre":
            result = self.num * 2.47105
        elif unit == "square_kilometer":
            result = self.num / 100
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Square Kilometer
class SquareKilometer(Area):
    """
    A class for converting areas from square kilometers to other units.

    Methods:
    --------
    square_kilometer_to(self, unit: str) -> Union[float, str]
        Converts the area from square kilometers to the specified unit.
    """

    def square_kilometer_to(self, unit: str) -> Union[float, str]:
        """
        Converts the area from square kilometers to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'square_centimeter', 'square_foot', 'square_yard', 'square_meter', 'acre', and 'hectare'.

        Returns:
        --------
        Union[float, str]
            The converted area value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "square_centimeter":
            result = self.num * 1e10
        elif unit == "square_foot":
            result = self.num * 1.076e7
        elif unit == "square_yard":
            result = self.num * 1.196e6
        elif unit == "square_meter":
            result = self.num * 1e6
        elif unit == "acre":
            result = self.num * 247.105
        elif unit == "hectare":
            result = self.num * 100
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)
