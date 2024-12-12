"""
This script provides a function to convert various electrical measurements between different units of electricity.

The `electricity_converter` function accepts an electrical quantity and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of electrical units and can take additional parameters such as resistance, current, voltage, time, or frequency 
to handle conversions that depend on these quantities. The function leverages the `electricity_formulas` module for the actual conversion logic.

### Supported Units:
- "ampere" (Electric Current)
- "volt" (Voltage)
- "ohm" (Resistance)
- "coulomb" (Electric Charge)
- "watt" (Power)
- "kilowatt" (Power)
- "farad" (Capacitance)
- "henry" (Inductance)
- "siemens" (Conductance)

### Main Function:
- `electricity_converter(elec: float, from_unit: str, to_unit: str, resistance: float = None, current: float = None, voltage: float = None, time: float = None, freq: float = None, with_unit: bool = False) -> Union[float, str]`

  Converts the input electrical quantity (`elec`) from a given unit (`from_unit`) to a target unit (`to_unit`). 
  For certain conversions, additional parameters such as `resistance`, `current`, `voltage`, `time`, or `freq` 
  may be required to perform the calculation. The `with_unit` parameter allows for an optional string output 
  that includes the unit in the result.

### Humanized Input:
- If `humanized_input` is set to `True`, the function allows more user-friendly input for units. 
  For example, the user can write "Ohm" instead of "ohm" or "Volt" instead of "volt".

### Example Usage:
- Converting 10 amperes to watts with a voltage of 220 volts:
    ```python
    electricity_converter(10, "ampere", "watt", voltage=220)
    ```
- Converting 500 watts to kilowatts with the unit in the result:
    ```python
    electricity_converter(500, "watt", "kilowatt", with_unit=True)
    ```
- Converting 100 volts to amperes with a resistance of 50 ohms:
    ```python
    electricity_converter(100, "volt", "ampere", resistance=50)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

### Dependencies:
- The script uses the `electricity_formulas` module from the `formulas` package to perform the actual conversion operations.
"""

from typing import Union

from Metricus._formulas import electricity_formulas as ef
from Metricus.utilities import humanize_input, round_number

unit_list = [
    "ampere",
    "volt",
    "ohm",
    "coulomb",
    "watt",
    "kilowatt",
    "farad",
    "henry",
    "siemens",
]


def electricity_converter(
    elec: float,
    from_unit: str,
    to_unit: str,
    rounded_result: bool = False,
    humanized_input: bool = False,
    resistance: float = None,
    current: float = None,
    voltage: float = None,
    time: float = None,
    freq: float = None,
    with_unit: bool = False,
) -> Union[float, str]:
    """
    Converts an electrical measurement from one unit to another.

    Args:
        elec (float): The electrical quantity to be converted.
        from_unit (str): The unit of the electrical quantity to convert from. Must be one of the supported units in `unit_list`.
        to_unit (str): The unit to convert the electrical quantity to. Must be one of the supported units in `unit_list`.
        resistance (float, optional): The resistance value (in ohms) used for conversions requiring resistance. Defaults to None.
        current (float, optional): The current value (in amperes) used for conversions requiring current. Defaults to None.
        voltage (float, optional): The voltage value (in volts) used for conversions requiring voltage. Defaults to None.
        time (float, optional): The time value (in seconds) used for conversions requiring time. Defaults to None.
        freq (float, optional): The frequency value (in hertz) used for conversions requiring frequency. Defaults to None.
        with_unit (bool, optional): If True, the result will include the unit of measurement as a string. Defaults to False.
        humanized_input (bool, optional): If True, allows user-friendly input for units (e.g., "Ohm" instead of "ohm"). Defaults to False.

    Returns:
        Union[float, str]: The converted electrical quantity. If `with_unit` is True, the result will include the unit as a string;
                           otherwise, it will return the numeric value of the converted quantity.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    Example usage:
        electricity_converter(10, "ampere", "watt", voltage=220)
        # Converts 10 amperes to watts with a voltage of 220 volts.

        electricity_converter(500, "watt", "kilowatt", with_unit=True)
        # Converts 500 watts to kilowatts and includes the unit in the result.

        electricity_converter(100, "volt", "ampere", resistance=50)
        # Converts 100 volts to amperes with a resistance of 50 ohms.
    """
    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    elif from_unit == to_unit:
        result = round_number(elec) if rounded_result else elec

    elif from_unit == "ampere":
        result = ef.Ampere(elec, with_unit=with_unit).ampere_to(
            to_unit, resistance=resistance, voltage=voltage, time=time, freq=freq
        )

    elif from_unit == "volt":
        result = ef.Volt(elec, with_unit=with_unit).volt_to(
            to_unit, resistance=resistance, current=current, time=time, freq=freq
        )

    elif from_unit == "ohm":
        result = ef.Ohm(elec, with_unit=with_unit).ohm_to(
            to_unit, voltage=voltage, current=current, time=time, freq=freq
        )

    elif from_unit == "coulomb":
        result = ef.Coulomb(elec, with_unit=with_unit).coulomb_to(
            to_unit, current=current, time=time, voltage=voltage
        )

    elif from_unit == "watt":
        result = ef.Watt(elec, with_unit=with_unit).watt_to(
            to_unit, voltage=voltage, current=current
        )

    elif from_unit == "kilowatt":
        result = ef.Kilowatt(elec, with_unit=with_unit).kilowatt_to(
            to_unit, voltage=voltage, current=current, time=time
        )

    elif from_unit == "farad":
        result = ef.Farad(elec, with_unit=with_unit).farad_to(
            to_unit, voltage=voltage, current=current, time=time
        )

    elif from_unit == "henry":
        result = ef.Henry(elec, with_unit=with_unit).henry_to(
            to_unit, current=current, freq=freq, voltage=voltage
        )
    
    elif from_unit == "siemens":
        result = ef.Siemens(elec, with_unit=with_unit).siemens_to(
            to_unit, resistance=resistance
        )
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result

