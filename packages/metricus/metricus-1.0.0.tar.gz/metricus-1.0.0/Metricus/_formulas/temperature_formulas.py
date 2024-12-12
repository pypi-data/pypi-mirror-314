"""
This module provides classes for converting temperature between different units.

Classes:
    - TemperatureUnit: A base class for temperature conversions. It handles the temperature value and whether or not the unit should be included in the output.
    - Celsius: A class for converting temperature from Celsius (°C) to other units such as Kelvin (K), Fahrenheit (°F), and Rankine (°R).
    - Fahrenheit: A class for converting temperature from Fahrenheit (°F) to other units such as Celsius (°C), Kelvin (K), and Rankine (°R).
    - Kelvin: A class for converting temperature from Kelvin (K) to other units such as Celsius (°C), Fahrenheit (°F), and Rankine (°R).
    - Rankine: A class for converting temperature from Rankine (°R) to other units such as Celsius (°C), Kelvin (K), and Fahrenheit (°F).

Usage Example:
    # Create a Celsius object
    temp_celsius = Celsius(25, with_unit=True)
    # Convert 25 degrees Celsius to Fahrenheit
    result = temp_celsius.celsius_to('fahrenheit')
    print(result)  # Output: "77.0 °F"

    # Create a Fahrenheit object
    temp_fahrenheit = Fahrenheit(77, with_unit=False)
    # Convert 77 degrees Fahrenheit to Celsius
    result = temp_fahrenheit.fahrenheit_to('celsius')
    print(result)  # Output: 25.0

    # Create a Kelvin object
    temp_kelvin = Kelvin(273.15, with_unit=True)
    # Convert 273.15 Kelvin to Celsius
    result = temp_kelvin.kelvin_to('celsius')
    print(result)  # Output: "0.0 °C"

    # Create a Rankine object
    temp_rankine = Rankine(491.67, with_unit=True)
    # Convert 491.67 Rankine to Celsius
    result = temp_rankine.rankine_to('celsius')
    print(result)  # Output: "0.0 °C"
"""

from typing import Union


# Base class for temperature units
class TemperatureUnit:
    def __init__(self, num: float, with_unit: bool = False) -> None:
        """
        Initialize a temperature unit instance.
        :param num: The numerical value of the temperature.
        :param with_unit: Flag to include unit in the formatted result.
        """
        self.num = num
        self.with_unit = with_unit

    def format_result(self, result: float, unit: str) -> Union[float, str]:
        """
        Format the result with or without unit.
        :param result: The calculated temperature.
        :param unit: The unit of the result.
        :return: Formatted temperature with or without unit.
        """
        units_map = {
            "celsius": "°C",
            "fahrenheit": "°F",
            "kelvin": "°K",
            "rankine": "°R",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Celsius
class Celsius(TemperatureUnit):
    def celsius_to(self, unit: str) -> Union[float, str]:
        """
        Convert Celsius to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted temperature.
        """
        if unit == "kelvin":
            result = self.num + 273.15
        elif unit == "fahrenheit":
            result = (self.num * 9 / 5) + 32
        elif unit == "rankine":
            result = (self.num * 9 / 5) + 491.67
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Fahrenheit
class Fahrenheit(TemperatureUnit):
    def fahrenheit_to(self, unit: str) -> Union[float, str]:
        """
        Convert Fahrenheit to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted temperature.
        """
        if unit == "celsius":
            result = (self.num - 32) * 5 / 9
        elif unit == "kelvin":
            result = (self.num - 32) * 5 / 9 + 273.15
        elif unit == "rankine":
            result = self.num + 459.67
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Kelvin
class Kelvin(TemperatureUnit):
    def kelvin_to(self, unit: str) -> Union[float, str]:
        """
        Convert Kelvin to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted temperature.
        """
        if unit == "fahrenheit":
            result = (self.num - 273.15) * 9 / 5 + 32
        elif unit == "celsius":
            result = self.num - 273.15
        elif unit == "rankine":
            result = self.num * 9 / 5
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Rankine
class Rankine(TemperatureUnit):
    def rankine_to(self, unit: str) -> Union[float, str]:
        """
        Convert Rankine to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted temperature.
        """
        if unit == "celsius":
            result = (self.num - 491.67) * 5 / 9
        elif unit == "kelvin":
            result = self.num * 5 / 9
        elif unit == "fahrenheit":
            result = self.num - 459.67
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)
