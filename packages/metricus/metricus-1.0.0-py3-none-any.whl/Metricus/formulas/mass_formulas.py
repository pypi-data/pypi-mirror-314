"""
This module provides classes for converting weight between different units.

Classes:
    - WeightUnit: A base class for weight conversions. It handles the weight value and whether or not the unit should be included in the output.
    - Milligram: A class for converting weight from milligrams (mg) to other units such as carat (ct), gram (g), ounce (oz), pound (lb), kilogram (kg), stone (st), slug (sl), and tonne (t).
    - Carat: A class for converting weight from carats (ct) to other units such as milligrams (mg), gram (g), ounce (oz), pound (lb), kilogram (kg), stone (st), slug (sl), and tonne (t).
    - Gram: A class for converting weight from grams (g) to other units such as milligrams (mg), carat (ct), ounce (oz), pound (lb), kilogram (kg), stone (st), slug (sl), and tonne (t).
    - Ounce: A class for converting weight from ounces (oz) to other units such as milligrams (mg), carat (ct), gram (g), pound (lb), kilogram (kg), stone (st), slug (sl), and tonne (t).
    - Pound: A class for converting weight from pounds (lb) to other units such as milligrams (mg), carat (ct), gram (g), ounce (oz), kilogram (kg), stone (st), slug (sl), and tonne (t).
    - Kilogram: A class for converting weight from kilograms (kg) to other units such as milligrams (mg), carat (ct), gram (g), ounce (oz), pound (lb), stone (st), slug (sl), and tonne (t).
    - Stone: A class for converting weight from stones (st) to other units such as milligrams (mg), carat (ct), gram (g), ounce (oz), pound (lb), kilogram (kg), slug (sl), and tonne (t).
    - Slug: A class for converting weight from slugs (sl) to other units such as milligrams (mg), carat (ct), gram (g), ounce (oz), pound (lb), kilogram (kg), stone (st), and tonne (t).
    - Tonne: A class for converting weight from tonnes (t) to other units such as milligrams (mg), carat (ct), gram (g), ounce (oz), pound (lb), kilogram (kg), stone (st), slug (sl).

Usage Example:
    # Create a Milligram object
    weight_milligram = Milligram(5000, with_unit=True)
    # Convert 5000 milligrams to grams
    result = weight_milligram.milligram_to('gram')
    print(result)  # Output: "5.0 g"

    # Create a Carat object
    weight_carat = Carat(100, with_unit=False)
    # Convert 100 carats to grams
    result = weight_carat.carat_to('gram')
    print(result)  # Output: 20.0

    # Create a Pound object
    weight_pound = Pound(150, with_unit=True)
    # Convert 150 pounds to kilograms
    result = weight_pound.pound_to('kilogram')
    print(result)  # Output: "68.1818 kg"

    # Create a Tonne object
    weight_tonne = Tonne(5, with_unit=True)
    # Convert 5 tonnes to pounds
    result = weight_tonne.tonne_to('pound')
    print(result)  # Output: "11023.1 lb"
"""

from typing import Union


# Base class for weight units
class WeightUnit:
    def __init__(self, num: float, with_unit: bool = False) -> None:
        """
        Initialize a weight unit instance.
        :param num: The numerical value of the weight.
        :param with_unit: Flag to include unit in the formatted result.
        """
        self.num = num
        self.with_unit = with_unit

    def format_result(self, result: float, unit: str) -> Union[float, str]:
        """
        Format the result with or without unit.
        :param result: The calculated weight.
        :param unit: The unit of the result.
        :return: Formatted weight with or without unit.
        """
        units_map = {
            "milligram": "mg",
            "carat": "ct",
            "gram": "g",
            "ounce": "oz",
            "pound": "lb",
            "kilogram": "kg",
            "stone": "st",
            "slug": "sl",
            "tonne": "t",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Milligram
class Milligram(WeightUnit):
    def milligram_to(self, unit: str) -> Union[float, str]:
        """
        Convert milligrams to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "carat":
            result = self.num / 200
        elif unit == "gram":
            result = self.num / 1000
        elif unit == "ounce":
            result = self.num / 28_349.5
        elif unit == "pound":
            result = self.num / 453_592
        elif unit == "kilogram":
            result = self.num / 1_000_000
        elif unit == "stone":
            result = self.num / 6_350_290
        elif unit == "slug":
            result = self.num / 14_593_900
        elif unit == "tonne":
            result = self.num / 1_000_000_000
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Carat
class Carat(WeightUnit):
    def carat_to(self, unit: str) -> Union[float, str]:
        """
        Convert carats to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 200
        elif unit == "gram":
            result = self.num / 5
        elif unit == "ounce":
            result = self.num / 141.7476
        elif unit == "pound":
            result = self.num / 2267.96
        elif unit == "kilogram":
            result = self.num / 5000
        elif unit == "stone":
            result = self.num / 6350.29
        elif unit == "slug":
            result = (self.num * 200) / 1_000_000 / 14.5939
        elif unit == "tonne":
            result = self.num / 5_000_000
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Gram
class Gram(WeightUnit):
    def gram_to(self, unit: str) -> Union[float, str]:
        """
        Convert grams to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 1000
        elif unit == "carat":
            result = self.num * 5
        elif unit == "ounce":
            result = self.num / 28.3495
        elif unit == "pound":
            result = self.num / 453.592
        elif unit == "kilogram":
            result = self.num / 1000
        elif unit == "stone":
            result = self.num / 6_350.29
        elif unit == "slug":
            result = self.num / 14_593.9
        elif unit == "tonne":
            result = self.num / 1_000_000
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Ounce
class Ounce(WeightUnit):
    def ounce_to(self, unit: str) -> Union[float, str]:
        """
        Convert ounces to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 28_349.5
        elif unit == "carat":
            result = self.num * 141.7476
        elif unit == "gram":
            result = self.num * 28.3495
        elif unit == "pound":
            result = self.num / 16
        elif unit == "kilogram":
            result = self.num / 35.274
        elif unit == "stone":
            result = self.num / 224
        elif unit == "slug":
            result = self.num / 514.78
        elif unit == "tonne":
            result = self.num / 35_274.96
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Pound
class Pound(WeightUnit):
    def pound_to(self, unit: str) -> Union[float, str]:
        """
        Convert pounds to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 453_592
        elif unit == "carat":
            result = self.num * 2267.96
        elif unit == "gram":
            result = self.num * 453.592
        elif unit == "ounce":
            result = self.num * 16
        elif unit == "kilogram":
            result = self.num / 2.20462
        elif unit == "stone":
            result = self.num / 14
        elif unit == "slug":
            result = self.num / 32.174
        elif unit == "tonne":
            result = self.num / 2204.62
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Kilogram
class Kilogram(WeightUnit):
    def kilogram_to(self, unit: str) -> Union[float, str]:
        """
        Convert kilograms to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 1_000_000
        elif unit == "carat":
            result = self.num * 5000
        elif unit == "gram":
            result = self.num * 1000
        elif unit == "ounce":
            result = self.num * 35.274
        elif unit == "pound":
            result = self.num * 2.20462
        elif unit == "stone":
            result = self.num / 6.35
        elif unit == "slug":
            result = self.num / 14.5939
        elif unit == "tonne":
            result = self.num / 1000
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Stone
class Stone(WeightUnit):
    def stone_to(self, unit: str) -> Union[float, str]:
        """
        Convert stones to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 6_350_290
        elif unit == "carat":
            result = self.num * 31_751.45
        elif unit == "gram":
            result = self.num * 6_350.29
        elif unit == "ounce":
            result = self.num * 224
        elif unit == "pound":
            result = self.num * 14
        elif unit == "kilogram":
            result = self.num * 6.35029
        elif unit == "slug":
            result = self.num * (6.35029 / 14.5939)
        elif unit == "tonne":
            result = self.num * 0.15747
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Slug
class Slug(WeightUnit):
    def slug_to(self, unit: str) -> Union[float, str]:
        """
        Convert slugs to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 14_593_900
        elif unit == "carat":
            result = self.num * 72_969.5
        elif unit == "gram":
            result = self.num * 14_593.9
        elif unit == "ounce":
            result = self.num * 514.78
        elif unit == "pound":
            result = self.num * 32.174
        elif unit == "kilogram":
            result = self.num * 14.5939
        elif unit == "stone":
            result = self.num * (14.5939 / 6.35029)
        elif unit == "tonne":
            result = self.num * (14.5939 / 1000)
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Tonne
class Tonne(WeightUnit):
    def tonne_to(self, unit: str) -> Union[float, str]:
        """
        Convert tonnes to the specified unit.
        :param unit: The unit to convert to.
        :return: Converted weight.
        """
        if unit == "milligram":
            result = self.num * 1_000_000_000
        elif unit == "carat":
            result = self.num * 5_000_000
        elif unit == "gram":
            result = self.num * 1_000_000
        elif unit == "ounce":
            result = self.num * 35_274
        elif unit == "pound":
            result = self.num * 2204.62
        elif unit == "kilogram":
            result = self.num * 1000
        elif unit == "stone":
            result = self.num * 157.473
        elif unit == "slug":
            result = self.num * 68.5218
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)
