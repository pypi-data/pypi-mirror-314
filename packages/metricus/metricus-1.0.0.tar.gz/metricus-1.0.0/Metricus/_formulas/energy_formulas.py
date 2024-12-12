"""
This module provides classes for converting energy between different units.

Classes:

    - EnergyUnit: A base class for energy conversions. It handles the energy value and whether or not the unit should be included in the output.
    - Electronvolt: A class for converting energy from electronvolts (eV) to other units such as calories (cal), joules (J), British thermal units (BTU), kilocalories (kcal), and kilowatt-hours (kWh).
    - Calorie: A class for converting energy from calories (cal) to other units such as electronvolts (eV), joules (J), British thermal units (BTU), kilocalories (kcal), and kilowatt-hours (kWh).
    - Joule: A class for converting energy from joules (J) to other units such as electronvolts (eV), calories (cal), British thermal units (BTU), kilocalories (kcal), and kilowatt-hours (kWh).
    - BritishThermalUnit: A class for converting energy from British thermal units (BTU) to other units such as electronvolts (eV), calories (cal), joules (J), kilocalories (kcal), and kilowatt-hours (kWh).
    - Kilocalorie: A class for converting energy from kilocalories (kcal) to other units such as electronvolts (eV), calories (cal), joules (J), British thermal units (BTU), and kilowatt-hours (kWh).
    - KilowattHour: A class for converting energy from kilowatt-hours (kWh) to other units such as electronvolts (eV), calories (cal), joules (J), British thermal units (BTU), and kilocalories (kcal).

Usage Example:

    # Create an Electronvolt object
    energy_ev = Electronvolt(1e20, with_unit=True)

    # Convert 1e20 electronvolts to joules
    result = energy_ev.electronvolt_to('joule')
    print(result)  # Output: "16.0218 J"

    # Create a Calorie object
    energy_cal = Calorie(100, with_unit=True)

    # Convert 100 calories to joules
    result = energy_cal.calorie_to('joule')
    print(result)  # Output: "418.4 J"

    # Create a Joule object
    energy_joule = Joule(1000, with_unit=True)

    # Convert 1000 joules to kilowatt-hours
    result = energy_joule.joule_to('kilowatt_hour')
    print(result)  # Output: "2.77778e-4 kWh"

    # Create a BritishThermalUnit object
    energy_btu = BritishThermalUnit(1, with_unit=True)

    # Convert 1 BTU to kilocalories
    result = energy_btu.btu_to('kilocalorie')
    print(result)  # Output: "0.252164 kcal"

    # Create a Kilocalorie object
    energy_kcal = Kilocalorie(500, with_unit=True)

    # Convert 500 kilocalories to joules
    result = energy_kcal.kilocalorie_to('joule')
    print(result)  # Output: "2092000 J"

    # Create a KilowattHour object
    energy_kwh = KilowattHour(2, with_unit=True)

    # Convert 2 kilowatt-hours to joules
    result = energy_kwh.kilowatt_hour_to('joule')
    print(result)  # Output: "7.2e6 J"
"""

from typing import Union


# Base class for Energy Units
class EnergyUnit:
    """
    A base class for representing and converting energy units.

    Attributes:
    -----------
    num : float
        The numerical value of the energy unit.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `EnergyUnit` instance with a numerical value and an optional flag for including units in the result.
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
            The numerical result of the energy conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        units_map = {
            "electronvolt": "eV",
            "calorie": "cal",
            "joule": "J",
            "btu": "BTU",
            "kilocalorie": "kcal",
            "kilowatt_hour": "kWh",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Electronvolt
class Electronvolt(EnergyUnit):
    """
    A class for converting energy from electronvolts to other units.

    Methods:
    --------
    electronvolt_to(self, unit: str) -> Union[float, str]
        Converts the energy from electronvolts to the specified unit.
    """

    def electronvolt_to(self, unit: str) -> Union[float, str]:
        """
        Converts the energy from electronvolts to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'calorie', 'joule', 'btu', 'kilocalorie', and 'kilowatt_hour'.

        Returns:
        --------
        Union[float, str]
            The converted energy value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "calorie":
            result = self.num * 1.60218e-19 / 4.184
        elif unit == "joule":
            result = self.num * 1.60218e-19
        elif unit == "btu":
            result = self.num * 1.60218e-19 / 1055.06
        elif unit == "kilocalorie":
            result = self.num * 1.60218e-19 / (4.184 * 1000)
        elif unit == "kilowatt_hour":
            result = self.num * 1.60218e-19 / 3.6e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Calorie
class Calorie(EnergyUnit):
    """
    A class for converting energy from calories to other units.

    Methods:
    --------
    calorie_to(self, unit: str) -> Union[float, str]
        Converts the energy from calories to the specified unit.
    """

    def calorie_to(self, unit: str) -> Union[float, str]:
        """
        Converts the energy from calories to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'electronvolt', 'joule', 'btu', 'kilocalorie', and 'kilowatt_hour'.

        Returns:
        --------
        Union[float, str]
            The converted energy value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "electronvolt":
            result = self.num * 4.184 / 1.60218e-19
        elif unit == "joule":
            result = self.num * 4.184
        elif unit == "btu":
            result = self.num * 4.184 / 1055.06
        elif unit == "kilocalorie":
            result = self.num / 1000
        elif unit == "kilowatt_hour":
            result = self.num * 4.184 / 3.6e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Joule
class Joule(EnergyUnit):
    """
    A class for converting energy from joules to other units.

    Methods:
    --------
    joule_to(self, unit: str) -> Union[float, str]
        Converts the energy from joules to the specified unit.
    """

    def joule_to(self, unit: str) -> Union[float, str]:
        """
        Converts the energy from joules to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'electronvolt', 'calorie', 'btu', 'kilocalorie', and 'kilowatt_hour'.

        Returns:
        --------
        Union[float, str]
            The converted energy value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "electronvolt":
            result = self.num / 1.60218e-19
        elif unit == "calorie":
            result = self.num / 4.184
        elif unit == "btu":
            result = self.num / 1055.06
        elif unit == "kilocalorie":
            result = self.num / (4.184 * 1000)
        elif unit == "kilowatt_hour":
            result = self.num / 3.6e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# British Thermal Unit
class BritishThermalUnit(EnergyUnit):
    """
    A class for converting energy from British Thermal Units (BTU) to other units.

    Methods:
    --------
    btu_to(self, unit: str) -> Union[float, str]
        Converts the energy from British Thermal Units to the specified unit.
    """

    def btu_to(self, unit: str) -> Union[float, str]:
        """
        Converts the energy from British Thermal Units to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'electronvolt', 'calorie', 'joule', 'kilocalorie', and 'kilowatt_hour'.

        Returns:
        --------
        Union[float, str]
            The converted energy value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "electronvolt":
            result = (self.num * 1055.06) / 1.60218e-19
        elif unit == "calorie":
            result = (self.num * 1055.06) / 4.184
        elif unit == "joule":
            result = self.num * 1055.06
        elif unit == "kilocalorie":
            result = (self.num * 1055.06) / (4.184 * 1000)
        elif unit == "kilowatt_hour":
            result = (self.num * 1055.06) / 3.6e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Kilocalorie
class Kilocalorie(EnergyUnit):
    """
    A class for converting energy from kilocalories to other units.

    Methods:
    --------
    kilocalorie_to(self, unit: str) -> Union[float, str]
        Converts the energy from kilocalories to the specified unit.
    """

    def kilocalorie_to(self, unit: str) -> Union[float, str]:
        """
        Converts the energy from kilocalories to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'electronvolt', 'calorie', 'joule', 'btu', and 'kilowatt_hour'.

        Returns:
        --------
        Union[float, str]
            The converted energy value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "electronvolt":
            result = (self.num * 4184) / 1.60218e-19
        elif unit == "calorie":
            result = self.num * 1000
        elif unit == "joule":
            result = self.num * 4184
        elif unit == "btu":
            result = (self.num * 4184) / 1055.06
        elif unit == "kilowatt_hour":
            result = (self.num * 4184) / 3.6e6
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)


# Kilowatt-hour
class KilowattHour(EnergyUnit):
    """
    A class for converting energy from kilowatt-hours to other units.

    Methods:
    --------
    kilowatt_hour_to(self, unit: str) -> Union[float, str]
        Converts the energy from kilowatt-hours to the specified unit.
    """

    def kilowatt_hour_to(self, unit: str) -> Union[float, str]:
        """
        Converts the energy from kilowatt-hours to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'electronvolt', 'calorie', 'joule', 'btu', and 'kilocalorie'.

        Returns:
        --------
        Union[float, str]
            The converted energy value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "electronvolt":
            result = (self.num * 3.6e6) / 1.60218e-19
        elif unit == "calorie":
            result = (self.num * 3.6e6) / 4.184
        elif unit == "joule":
            result = self.num * 3.6e6
        elif unit == "btu":
            result = (self.num * 3.6e6) / 1055.06
        elif unit == "kilocalorie":
            result = (self.num * 3.6e6) / (4.184 * 1000)
        else:
            raise ValueError("The measurement has an unknown unit")
        return self.format_result(result, unit)
