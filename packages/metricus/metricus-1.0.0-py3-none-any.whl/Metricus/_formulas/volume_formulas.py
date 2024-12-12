"""
This module provides classes for converting volume between different units.

Classes:

    - Volume: A base class for volume conversions. It handles the volume value and whether or not the unit should be included in the output.
    - Milliliter: A class for converting volume from milliliters (mL) to other units such as cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), pints (pt), quarts (qt), liters (L), gallons (gal), barrels (bbl), and cubic meters (m³).
    - CubicCentimeter: A class for converting volume from cubic centimeters (cm³) to other units such as milliliters (mL), fluid ounces (fl_oz), cups (cup), pints (pt), quarts (qt), liters (L), gallons (gal), barrels (bbl), and cubic meters (m³).
    - FluidOunce: A class for converting volume from fluid ounces (fl_oz) to other units such as milliliters (mL), cubic centimeters (cm³), cups (cup), pints (pt), quarts (qt), liters (L), gallons (gal), barrels (bbl), and cubic meters (m³).
    - Cup: A class for converting volume from cups (cup) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), pints (pt), quarts (qt), liters (L), gallons (gal), barrels (bbl), and cubic meters (m³).
    - Pint: A class for converting volume from pints (pt) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), quarts (qt), liters (L), gallons (gal), barrels (bbl), and cubic meters (m³).
    - Quart: A class for converting volume from quarts (qt) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), pints (pt), liters (L), gallons (gal), barrels (bbl), and cubic meters (m³).
    - Liter: A class for converting volume from liters (L) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), pints (pt), quarts (qt), gallons (gal), barrels (bbl), and cubic meters (m³).
    - Gallon: A class for converting volume from gallons (gal) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), pints (pt), quarts (qt), liters (L), barrels (bbl), and cubic meters (m³).
    - Barrel: A class for converting volume from barrels (bbl) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), pints (pt), quarts (qt), liters (L), gallons (gal), and cubic meters (m³).
    - CubicMeter: A class for converting volume from cubic meters (m³) to other units such as milliliters (mL), cubic centimeters (cm³), fluid ounces (fl_oz), cups (cup), pints (pt), quarts (qt), liters (L), gallons (gal), barrels (bbl).

Usage Example:

    # Create a Milliliter object
    volume_ml = Milliliter(1000, with_unit=True)

    # Convert 1000 milliliters to liters
    result = volume_ml.mL_to('L')
    print(result)  # Output: "1.0 L"

    # Create a CubicCentimeter object
    volume_cm3 = CubicCentimeter(500, with_unit=False)

    # Convert 500 cubic centimeters to fluid ounces
    result2 = volume_cm3.to('fl_oz')
    print(result2)  # Output: 16.907

    # Create a Gallon object
    volume_gal = Gallon(3, with_unit=True)

    # Convert 3 gallons to liters
    result3 = volume_gal.gal_to('L')
    print(result3)  # Output: "11.35623 L"
"""

from typing import Union


# Base class for volume units
class Volume:
    def __init__(self, num: float, with_unit: bool = False) -> None:
        """
        Initialize a volume unit instance.
        :param num: The numerical value of the volume.
        :param with_unit: Flag to include unit in the formatted result.
        """
        self.num = num
        self.with_unit = with_unit

    def format_result(self, result: float, unit: str) -> Union[float, str]:
        """
        Format the result with or without unit.
        :param result: The calculated volume.
        :param unit: The unit of the result.
        :return: Formatted volume with or without unit.
        """
        unit = unit.replace("cm3", "cm³")
        unit = unit.replace("m3", "m³")
        return f"{result} {unit}" if self.with_unit else result


# Milliliter
class Milliliter(Volume):
    def mL_to(self, unit: str) -> Union[float, str]:
        """
        Convert milliliters to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "cm³" or unit == "cm3":
            result = self.num
        elif unit == "fl_oz":
            result = self.num / 29.5735
        elif unit == "cup":
            result = self.num / 240
        elif unit == "pt":
            result = self.num / 473.176
        elif unit == "qt":
            result = self.num / 946.353
        elif unit == "L":
            result = self.num / 1000
        elif unit == "gal":
            result = self.num / 3785.41
        elif unit == "bbl":
            result = self.num / 119240
        elif unit == "m³" or unit == "m3":
            result = self.num / 1e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Cubic Centimeter
class CubicCentimeter(Volume):
    def to(self, unit: str) -> Union[float, str]:
        """
        Convert cubic centimeters to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        # cm³ is equivalent to mL
        return Milliliter(self.num, self.with_unit).to(unit)


# Fluid Ounce
class FluidOunce(Volume):
    def fl_oz_to(self, unit: str) -> Union[float, str]:
        """
        Convert fluid ounces to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 29.5735
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 29.5735
        elif unit == "cup":
            result = self.num / 8
        elif unit == "pt":
            result = self.num / 16
        elif unit == "qt":
            result = self.num / 32
        elif unit == "L":
            result = self.num / 33.814
        elif unit == "gal":
            result = self.num / 128
        elif unit == "bbl":
            result = self.num / 4032
        elif unit == "m3" or unit == "m3":
            result = self.num / 33814
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Cup
class Cup(Volume):
    def cup_to(self, unit: str) -> Union[float, str]:
        """
        Convert cups to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 240
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 240
        elif unit == "fl_oz":
            result = self.num * 8
        elif unit == "pt":
            result = self.num / 2
        elif unit == "qt":
            result = self.num / 4
        elif unit == "L":
            result = self.num / 4.22675
        elif unit == "gal":
            result = self.num / 16
        elif unit == "bbl":
            result = self.num / 5040
        elif unit == "m³" or unit == "m3":
            result = self.num / 4226.75
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Pint
class Pint(Volume):
    def pt_to(self, unit: str) -> Union[float, str]:
        """
        Convert pints to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 473.176
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 473.176
        elif unit == "fl_oz":
            result = self.num * 16
        elif unit == "cup":
            result = self.num * 2
        elif unit == "qt":
            result = self.num / 2
        elif unit == "L":
            result = self.num / 2.11338
        elif unit == "gal":
            result = self.num / 8
        elif unit == "bbl":
            result = self.num / 2016
        elif unit == "m³" or unit == "m3":
            result = self.num / 2113.38
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Quart
class Quart(Volume):
    def qt_to(self, unit: str) -> Union[float, str]:
        """
        Convert quarts to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 946.353
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 946.353
        elif unit == "fl_oz":
            result = self.num * 32
        elif unit == "cup":
            result = self.num * 4
        elif unit == "pt":
            result = self.num * 2
        elif unit == "L":
            result = self.num / 1.05669
        elif unit == "gal":
            result = self.num / 4
        elif unit == "bbl":
            result = self.num / 1008
        elif unit == "m³" or unit == "m3":
            result = self.num / 1056.69
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Liter
class Liter(Volume):
    def liter_to(self, unit: str) -> Union[float, str]:
        """
        Convert liters to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 1000
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 1000
        elif unit == "fl_oz":
            result = self.num * 33.814
        elif unit == "cup":
            result = self.num * 4.22675
        elif unit == "pt":
            result = self.num * 2.11338
        elif unit == "qt":
            result = self.num * 1.05669
        elif unit == "gal":
            result = self.num / 3.78541
        elif unit == "bbl":
            result = self.num / 119.24
        elif unit == "m³" or unit == "m3":
            result = self.num / 1000
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Gallon
class Gallon(Volume):
    def gal_to(self, unit: str) -> Union[float, str]:
        """
        Convert gallons to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 3785.41
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 3785.41
        elif unit == "fl_oz":
            result = self.num * 128
        elif unit == "cup":
            result = self.num * 16
        elif unit == "pt":
            result = self.num * 8
        elif unit == "qt":
            result = self.num * 4
        elif unit == "L":
            result = self.num * 3.78541
        elif unit == "bbl":
            result = self.num / 31.5
        elif unit == "m³" or unit == "m3":
            result = self.num / 264.172
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Barrel
class Barrel(Volume):
    def bbl_to(self, unit: str) -> Union[float, str]:
        """
        Convert barrels to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 119240
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 119240
        elif unit == "fl_oz":
            result = self.num * 4032
        elif unit == "cup":
            result = self.num * 5040
        elif unit == "pt":
            result = self.num * 2016
        elif unit == "qt":
            result = self.num * 1008
        elif unit == "L":
            result = self.num * 119.24
        elif unit == "gal":
            result = self.num * 31.5
        elif unit == "m³" or unit == "m3":
            result = self.num / 8.386
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Cubic Meter
class CubicMeter(Volume):
    def m3_to(self, unit: str) -> Union[float, str]:
        """
        Convert cubic meters to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted volume.
        """
        if unit == "mL":
            result = self.num * 1e6
        elif unit == "cm³" or unit == "cm3":
            result = self.num * 1e6
        elif unit == "fl_oz":
            result = self.num * 33814
        elif unit == "cup":
            result = self.num * 4226.75
        elif unit == "pt":
            result = self.num * 2113.38
        elif unit == "qt":
            result = self.num * 1056.69
        elif unit == "L":
            result = self.num * 1000
        elif unit == "gal":
            result = self.num * 264.172
        elif unit == "bbl":
            result = self.num * 264.172 / 31.5
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)
