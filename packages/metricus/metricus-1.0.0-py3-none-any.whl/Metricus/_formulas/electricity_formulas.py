"""
This module provides classes for converting electrical units between different measurements.

Classes:

    - ElectricalUnit: A base class for electrical unit conversions. It handles the unit value and whether or not the unit should be included in the output.
    - Ampere: A class for converting electric current from amperes (A) to other units such as volts (V), ohms (Ω), coulombs (C), watts (W), kilowatts (kW), henrys (H), and siemens (S).
    - Volt: A class for converting electric potential from volts (V) to other units such as amperes (A), ohms (Ω), coulombs (C), watts (W), kilowatts (kW), farads (F), and henrys (H).
    - Ohm: A class for converting electrical resistance from ohms (Ω) to other units such as amperes (A), volts (V), coulombs (C), watts (W), kilowatts (kW), farads (F), and henrys (H).
    - Coulomb: A class for converting electric charge from coulombs (C) to other units such as amperes (A), volts (V), and watts (W).
    - Watt: A class for converting power from watts (W) to other units such as amperes (A), volts (V), ohms (Ω), and kilowatts (kW).
    - Kilowatt: A class for converting power from kilowatts (kW) to other units such as watts (W), amperes (A), volts (V), ohms (Ω), and coulombs (C).
    - Farad: A class for converting capacitance from farads (F) to other units such as coulombs (C), volts (V), amperes (A), and ohms (Ω).
    - Henry: A class for converting inductance from henrys (H) to other units such as amperes (A), volts (V), ohms (Ω), and coulombs (C).
    - Siemens: A class for converting conductance from siemens (S) to other units such as amperes (A), volts (V), ohms (Ω), and watts (W).

Usage Example:

    # Create an Ampere object
    current = Ampere(10, with_unit=True)

    # Convert 10 amperes to volts, given the resistance is 5 ohms
    result = current.ampere_to('volt', resistance=5)
    print(result)  # Output: "50 V"

    # Create a Volt object
    voltage = Volt(20, with_unit=True)

    # Convert 20 volts to amperes, given the resistance is 4 ohms
    result = voltage.volt_to('ampere', resistance=4)
    print(result)  # Output: "5.0 A"

    # Create an Ohm object
    resistance = Ohm(10, with_unit=True)

    # Convert 10 ohms to amperes, given the voltage is 20 volts
    result = resistance.ohm_to('ampere', voltage=20)
    print(result)  # Output: "2.0 A"

    # Create a Coulomb object
    charge = Coulomb(10, with_unit=True)

    # Convert 10 coulombs to amperes, given the time is 2 seconds
    result = charge.coulomb_to('ampere', time=2)
    print(result)  # Output: "5.0 A"

    # Create a Watt object
    power = Watt(100, with_unit=True)

    # Convert 100 watts to amperes, given the voltage is 20 volts
    result = power.watt_to('ampere', voltage=20)
    print(result)  # Output: "5.0 A"

    # Create a Kilowatt object
    power_kw = Kilowatt(1, with_unit=True)

    # Convert 1 kilowatt to watts
    result = power_kw.kilowatt_to('watt')
    print(result)  # Output: "1000 W"

    # Create a Farad object
    capacitance = Farad(10, with_unit=True)

    # Convert 10 farads to coulombs, given the voltage is 5 volts
    result = capacitance.farad_to('coulomb', voltage=5)
    print(result)  # Output: "50.0 C"

    # Create a Henry object
    inductance = Henry(10, with_unit=True)

    # Convert 10 henries to amperes, given the voltage is 5 volts
    result = inductance.henry_to('ampere', voltage=5)
    print(result)  # Output: "0.5 A"

    # Create a Siemens object
    conductance = Siemens(10, with_unit=True)

    # Convert 10 siemens to amperes, given the voltage is 5 volts
    result = conductance.siemens_to('ampere', voltage=5)
    print(result)  # Output: "50.0 A"
"""

from typing import Union


# Base class for Electrical Units
class ElectricalUnit:
    """
    A base class for converting electrical units.

    Attributes:
    -----------
    num : float
        The numerical value of the electrical unit.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `ElectricalUnit` instance with a numerical value and an optional flag for including units in the result.
    format_result(self, result: float, unit: str) -> Union[float, str]
        Formats the result to include the appropriate unit if `with_unit` is set to `True`.
    raise_value_error(self, parameter: str) -> None
        Raises a ValueError indicating that the specified parameter value is needed for conversion.
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
            The numerical result of the electrical unit conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        unit_abbreviations = {
            "ampere": "A",
            "volt": "V",
            "ohm": "Ω",
            "coulomb": "C",
            "watt": "W",
            "kilowatt": "kW",
            "farad": "F",
            "henry": "H",
            "siemens": "S",
        }
        if self.with_unit:
            return f"{result} {unit_abbreviations.get(unit, unit)}"
        else:
            return result

    def raise_value_error(self, parameter: str) -> None:
        """
        Raises a ValueError indicating that the specified parameter value is needed for conversion.

        Parameters:
        -----------
        parameter : str
            The name of the parameter that is missing.

        Raises:
        -------
        ValueError
            Indicates that the specified parameter value is needed for conversion.
        """
        raise ValueError(f"{parameter} value needed for conversion.")


# Ampere
class Ampere(ElectricalUnit):
    """
    A class for converting electric current from amperes to other units.

    Methods:
    --------
    ampere_to(self, unit: str, resistance: float = None, voltage: float = None, time: float = None, freq: float = None) -> Union[float, str]
        Converts the current from amperes to the specified unit.
    """

    def ampere_to(
        self,
        unit: str,
        resistance: float = None,
        voltage: float = None,
        time: float = None,
        freq: float = None,
    ) -> Union[float, str]:
        """
        Converts the current from amperes to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'volt', 'ohm', 'coulomb', 'watt', 'kilowatt', 'henry', and 'siemens'.
        resistance : float, optional
            The resistance value in ohms, needed for conversions to volts or siemens.
        voltage : float, optional
            The voltage value in volts, needed for conversions to ohms, watts, kilowatts, or henrys.
        time : float, optional
            The time value in seconds, needed for conversion to coulombs.
        freq : float, optional
            The frequency value in hertz, needed for conversion to henrys.

        Returns:
        --------
        Union[float, str]
            The converted current value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        """
        result = None

        if unit == "volt":
            if resistance is not None:
                result = self.num * resistance
            else:
                self.raise_value_error("Resistance")

        elif unit == "ohm":
            if voltage is not None:
                result = voltage / self.num
            else:
                self.raise_value_error("Voltage")

        elif unit == "coulomb":
            if time is not None:
                result = self.num * time
            else:
                self.raise_value_error("Time")

        elif unit == "watt":
            if voltage is not None:
                result = self.num * voltage
            else:
                self.raise_value_error("Voltage")

        elif unit == "kilowatt":
            if voltage is not None:
                result = (self.num * voltage) / 1000
            else:
                self.raise_value_error("Voltage")

        elif unit == "henry":
            if voltage is not None and freq is not None:
                result = voltage / (self.num * freq)
            else:
                self.raise_value_error("Voltage and frequency")

        elif unit == "siemens":
            if resistance is not None:
                result = 1 / resistance
            else:
                self.raise_value_error("Resistance")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Volt
class Volt(ElectricalUnit):
    """
    A class for converting electrical potential from volts to other units.

    Methods:
    --------
    volt_to(self, unit: str, resistance: float = None, current: float = None, time: float = None, freq: float = None) -> Union[float, str]
        Converts the electrical potential from volts to the specified unit.
    """

    def volt_to(
        self,
        unit: str,
        resistance: float = None,
        current: float = None,
        time: float = None,
        freq: float = None,
    ) -> Union[float, str]:
        """
        Converts the electrical potential from volts to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'ampere', 'ohm', 'coulomb', 'watt', 'kilowatt', 'farad', 'henry', and 'siemens'.
        resistance : float, optional
            The resistance value in ohms, needed for conversions to amperes or farads.
        current : float, optional
            The current value in amperes, needed for conversions to ohms, coulombs, watts, kilowatts, or henrys.
        time : float, optional
            The time value in seconds, needed for conversion to coulombs.
        freq : float, optional
            The frequency value in hertz, needed for conversion to farads or henrys.

        Returns:
        --------
        Union[float, str]
            The converted voltage value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        """
        result = None

        if unit == "ampere":
            if resistance is not None:
                result = self.num / resistance
            else:
                self.raise_value_error("Resistance")

        elif unit == "ohm":
            if current is not None:
                result = self.num / current
            else:
                self.raise_value_error("Current")

        elif unit == "coulomb":
            if current is not None and time is not None:
                result = current * time
            else:
                self.raise_value_error("Current and time")

        elif unit == "watt":
            if current is not None:
                result = self.num * current
            else:
                self.raise_value_error("Current")

        elif unit == "kilowatt":
            if current is not None:
                result = (self.num * current) / 1000
            else:
                self.raise_value_error("Current")

        elif unit == "farad":
            if resistance is not None and freq is not None:
                result = 1 / (2 * 3.14159 * resistance * freq)
            else:
                self.raise_value_error("Resistance and frequency")

        elif unit == "henry":
            if current is not None and freq is not None:
                result = self.num / (2 * 3.14159 * current * freq)
            else:
                self.raise_value_error("Current and frequency")

        elif unit == "siemens":
            if resistance is not None:
                result = 1 / resistance
            else:
                self.raise_value_error("Resistance")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Ohm
class Ohm(ElectricalUnit):
    """
    A class for converting electrical resistance from ohms to other units.

    Methods:
    --------
    ohm_to(self, unit: str, current: float = None, voltage: float = None, time: float = None, freq: float = None) -> Union[float, str]
        Converts the resistance from ohms to the specified unit.
    """

    def ohm_to(
        self,
        unit: str,
        current: float = None,
        voltage: float = None,
        time: float = None,
        freq: float = None,
    ) -> Union[float, str]:
        """
        Converts the resistance from ohms to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'ampere', 'volt', 'coulomb', 'watt', 'kilowatt', 'farad', 'henry', and 'siemens'.
        current : float, optional
            The current value in amperes, needed for conversions to volts, coulombs, watts, or kilowatts.
        voltage : float, optional
            The voltage value in volts, needed for conversions to amperes.
        time : float, optional
            The time value in seconds, needed for conversion to coulombs.
        freq : float, optional
            The frequency value in hertz, needed for conversion to farads or henrys.

        Returns:
        --------
        Union[float, str]
            The converted resistance value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        """
        result = None

        if unit == "ampere":
            if voltage is not None:
                result = voltage / self.num
            else:
                self.raise_value_error("Voltage")

        elif unit == "volt":
            if current is not None:
                result = self.num * current
            else:
                self.raise_value_error("Current")

        elif unit == "coulomb":
            if current is not None and time is not None:
                result = current * time
            else:
                self.raise_value_error("Current and time")

        elif unit == "watt":
            if current is not None:
                result = self.num * (current**2)
            else:
                self.raise_value_error("Current")

        elif unit == "kilowatt":
            if current is not None:
                result = (self.num * (current**2)) / 1000
            else:
                self.raise_value_error("Current")

        elif unit == "farad":
            if freq is not None:
                result = 1 / (2 * 3.14159 * self.num * freq)
            else:
                self.raise_value_error("Frequency")

        elif unit == "henry":
            if freq is not None:
                result = self.num / (2 * 3.14159 * freq)
            else:
                self.raise_value_error("Frequency")

        elif unit == "siemens":
            result = 1 / self.num

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Coulomb
class Coulomb(ElectricalUnit):
    """
    A class for converting electric charge from coulombs to other units.

    Methods:
    --------
    coulomb_to(self, unit: str, current: float = None, voltage: float = None, time: float = None, capacitance: float = None) -> Union[float, str]
        Converts the charge from coulombs to the specified unit.
    """

    def coulomb_to(
        self,
        unit: str,
        current: float = None,
        voltage: float = None,
        time: float = None,
        capacitance: float = None,
    ) -> Union[float, str]:
        """
        Converts the charge from coulombs to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'ampere', 'volt', and 'watt'.
        current : float, optional
            The current value in amperes, needed for conversion to watts.
        voltage : float, optional
            The voltage value in volts, needed for conversion to watts.
        time : float, optional
            The time value in seconds, needed for conversion to amperes.
        capacitance : float, optional
            The capacitance value in farads, needed for conversion to volts.

        Returns:
        --------
        Union[float, str]
            The converted charge value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        NotImplementedError
            If conversion to the specified unit is not supported yet.
        """
        result = None

        if unit == "ampere":
            if time is not None and time != 0:
                result = self.num / time
            else:
                self.raise_value_error("A valid, non-zero time")

        elif unit == "volt":
            if capacitance is not None and capacitance != 0:
                result = self.num / capacitance
            else:
                self.raise_value_error("A valid, non-zero capacitance")

        elif unit == "watt":
            if voltage is not None and current is not None:
                result = voltage * current
            else:
                self.raise_value_error("Both voltage and current")

        elif unit in ["ohm", "kilowatt", "farad", "henry", "siemens"]:
            raise NotImplementedError(f"Conversion to {unit} is not supported yet.")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Watt
class Watt(ElectricalUnit):
    """
    A class for converting power from watts to other units.

    Methods:
    --------
    watt_to(self, unit: str, current: float = None, voltage: float = None, time: float = None) -> Union[float, str]
        Converts the power from watts to the specified unit.
    """

    def watt_to(
        self,
        unit: str,
        current: float = None,
        voltage: float = None,
        time: float = None,
    ) -> Union[float, str]:
        """
        Converts the power from watts to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'ampere', 'volt', 'ohm', 'coulomb', and 'kilowatt'.
        current : float, optional
            The current value in amperes, needed for conversions to volts or ohms.
        voltage : float, optional
            The voltage value in volts, needed for conversions to amperes.
        time : float, optional
            The time value in seconds, needed for conversion to coulombs.

        Returns:
        --------
        Union[float, str]
            The converted power value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        NotImplementedError
            If conversion to the specified unit is not supported yet.
        """
        result = None

        if unit == "ampere":
            if voltage is not None:
                result = self.num / voltage
            else:
                self.raise_value_error("Voltage")

        elif unit == "volt":
            if current is not None:
                result = self.num / current
            else:
                self.raise_value_error("Current")

        elif unit == "ohm":
            if current is not None:
                result = self.num / (current**2)
            else:
                self.raise_value_error("Current")

        elif unit == "coulomb":
            if time is not None:
                result = self.num * time
            else:
                self.raise_value_error("Time")

        elif unit == "kilowatt":
            result = self.num / 1000

        elif unit in ["farad", "henry", "siemens"]:
            raise NotImplementedError(f"Conversion to {unit} is not supported yet.")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Kilowatt
class Kilowatt(ElectricalUnit):
    """
    A class for converting power from kilowatts to other units.

    Methods:
    --------
    kilowatt_to(self, unit: str, current: float = None, voltage: float = None, time: float = None) -> Union[float, str]
        Converts the power from kilowatts to the specified unit.
    """

    def kilowatt_to(
        self,
        unit: str,
        current: float = None,
        voltage: float = None,
        time: float = None,
    ) -> Union[float, str]:
        """
        Converts the power from kilowatts to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'watt', 'ampere', 'volt', 'ohm', and 'coulomb'.
        current : float, optional
            The current value in amperes, needed for conversions to volts or ohms.
        voltage : float, optional
            The voltage value in volts, needed for conversions to amperes.
        time : float, optional
            The time value in seconds, needed for conversion to coulombs.

        Returns:
        --------
        Union[float, str]
            The converted power value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        NotImplementedError
            If conversion to the specified unit is not supported yet.
        """
        result = None

        if unit == "watt":
            result = self.num * 1000

        elif unit == "ampere":
            if voltage is not None:
                result = (self.num * 1000) / voltage
            else:
                self.raise_value_error("Voltage")

        elif unit == "volt":
            if current is not None:
                result = (self.num * 1000) / current
            else:
                self.raise_value_error("Current")

        elif unit == "ohm":
            if current is not None:
                result = (self.num * 1000) / (current**2)
            else:
                self.raise_value_error("Current")

        elif unit == "coulomb":
            if time is not None:
                result = (self.num * 1000) * time
            else:
                self.raise_value_error("Time")

        elif unit in ["farad", "henry", "siemens"]:
            raise NotImplementedError(f"Conversion to {unit} is not supported yet.")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Farad
class Farad(ElectricalUnit):
    """
    A class for converting electrical capacitance from farads to other units.

    Methods:
    --------
    farad_to(self, unit: str, current: float = None, voltage: float = None, time: float = None, charge: float = None) -> Union[float, str]
        Converts the capacitance from farads to the specified unit.
    """

    def farad_to(
        self,
        unit: str,
        current: float = None,
        voltage: float = None,
        time: float = None,
        charge: float = None,
    ) -> Union[float, str]:
        """
        Converts the capacitance from farads to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'coulomb', 'volt', 'ampere', and 'ohm'.
        current : float, optional
            The current value in amperes, needed for conversions to ohms.
        voltage : float, optional
            The voltage value in volts, needed for conversions to coulombs or amperes.
        time : float, optional
            The time value in seconds, needed for conversion to amperes.
        charge : float, optional
            The charge value in coulombs, needed for conversion to volts.

        Returns:
        --------
        Union[float, str]
            The converted capacitance value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        NotImplementedError
            If conversion to the specified unit is not supported yet.
        """
        result = None

        if unit == "coulomb":
            if voltage is not None:
                result = self.num * voltage
            else:
                self.raise_value_error("Voltage")

        elif unit == "volt":
            if charge is not None:
                result = charge / self.num
            else:
                self.raise_value_error("Charge")

        elif unit == "ampere":
            if voltage is not None and time is not None:
                result = self.num * (voltage / time)
            else:
                self.raise_value_error("Voltage and time")

        elif unit == "ohm":
            if current is not None:
                result = self.num / (current**2)
            else:
                self.raise_value_error("Current")

        elif unit in ["watt", "kilowatt", "henry", "siemens"]:
            raise NotImplementedError(f"Conversion to {unit} is not supported yet.")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Henry
class Henry(ElectricalUnit):
    """
    A class for converting electrical inductance from henries to other units.

    Methods:
    --------
    henry_to(self, unit: str, current: float = None, voltage: float = None, time: float = None, charge: float = None) -> Union[float, str]
        Converts the inductance from henries to the specified unit.
    """

    def henry_to(
        self,
        unit: str,
        freq: float = None,
        current: float = None,
        voltage: float = None,
        time: float = None,
        charge: float = None,
    ) -> Union[float, str]:
        """
        Converts the inductance from henries to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'ampere', 'volt', 'ohm', 'coulomb', 'watt', and 'kilowatt'.
        current : float, optional
            The current value in amperes, needed for conversions to volts or watts.
        voltage : float, optional
            The voltage value in volts, needed for conversions to amperes or coulombs.
        time : float, optional
            The time value in seconds, needed for conversions to ohms or coulombs.
        charge : float, optional
            The charge value in coulombs, needed for conversion to volts.

        Returns:
        --------
        Union[float, str]
            The converted inductance value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        NotImplementedError
            If conversion to the specified unit is not supported yet.
        """
        result = None

        if unit == "ampere":
            if voltage is not None:
                result = voltage / self.num
            else:
                self.raise_value_error("Voltage")

        elif unit == "volt":
            if current is not None:
                result = self.num * current
            else:
                self.raise_value_error("Current")

        elif unit == "ohm":
            if time is not None:
                result = self.num / time
            else:
                self.raise_value_error("Time")

        elif unit == "coulomb":
            if voltage is not None and time is not None:
                result = (voltage * time) / self.num
            else:
                self.raise_value_error("Voltage and time")

        elif unit == "watt":
            if current is not None:
                result = self.num * (current**2)
            else:
                self.raise_value_error("Current")

        elif unit == "kilowatt":
            if current is not None:
                result = (self.num * (current**2)) / 1000
            else:
                self.raise_value_error("Current")

        elif unit in ["farad", "siemens"]:
            raise NotImplementedError(f"Conversion to {unit} is not supported yet.")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)


# Siemens
class Siemens(ElectricalUnit):
    """
    A class for converting electrical conductance from siemens to other units.

    Methods:
    --------
    siemens_to(self, unit: str, current: float = None, voltage: float = None, time: float = None, charge: float = None) -> Union[float, str]
        Converts the conductance from siemens to the specified unit.
    """

    def siemens_to(
        self,
        unit: str,
        current: float = None,
        voltage: float = None,
        time: float = None,
        resistance: float = None,
        charge: float = None,
    ) -> Union[float, str]:
        """
        Converts the conductance from siemens to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'ampere', 'volt', 'ohm', 'coulomb', 'watt', and 'kilowatt'.
        current : float, optional
            The current value in amperes, needed for conversions to volts, coulombs, or watts.
        voltage : float, optional
            The voltage value in volts, needed for conversions to amperes, watts, or kilowatts.
        time : float, optional
            The time value in seconds, needed for conversion to coulombs.
        charge : float, optional
            The charge value in coulombs, not used in current implementations.

        Returns:
        --------
        Union[float, str]
            The converted conductance value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If a required parameter for the conversion is missing or if an invalid unit is provided.
        NotImplementedError
            If conversion to the specified unit is not supported yet.
        """
        result = None

        if unit == "ampere":
            if voltage is not None:
                result = voltage * self.num
            else:
                self.raise_value_error("Voltage")

        elif unit == "volt":
            if current is not None:
                result = current / self.num
            else:
                self.raise_value_error("Current")

        elif unit == "ohm":
            result = 1 / self.num

        elif unit == "coulomb":
            if current is not None and time is not None:
                result = current * time
            else:
                self.raise_value_error("Current and time")

        elif unit == "watt":
            if current is not None and voltage is not None:
                result = voltage * current
            else:
                self.raise_value_error("Voltage and current")

        elif unit == "kilowatt":
            if current is not None and voltage is not None:
                result = (voltage * current) / 1000
            else:
                self.raise_value_error("Voltage and current")

        elif unit == "farad":
            raise NotImplementedError("Conversion to farad is not supported yet.")

        elif unit == "henry":
            raise NotImplementedError("Conversion to henry is not supported yet.")

        if result is None:
            raise ValueError("Invalid or unsupported unit provided.")

        return self.format_result(result, unit)
