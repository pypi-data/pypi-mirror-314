"""
This script provides a function to convert time between different units of measurement.

The `time_converter` function accepts a time value and converts it from one unit to another using predefined conversion formulas. 
It supports a wide range of time units, from smaller (milliseconds) to larger (centuries). The conversion is performed by leveraging 
the `time_formulas` module, which contains specific methods for handling each time unit.

### Supported Units:
- "millisecond"
- "second"
- "minute"
- "hour"
- "day"
- "week"
- "month"
- "year"
- "decade"
- "century"

### Main Function:
- `time_converter(time: float, from_unit: str, to_unit: str, rounded_result: bool = True, humanized_input: bool = False, with_unit: bool = False) -> Union[float, str]`

  Converts the input time (`time`) from a given unit (`from_unit`) to a target unit (`to_unit`). The function uses specific
  conversion logic to handle each unit type and ensure accurate conversions. Additional options allow rounding the result
  and enabling human-readable input formats.

### Parameters:
- `time` (float): The time value to be converted.
- `from_unit` (str): The source unit of the time to convert from.
- `to_unit` (str): The target unit to convert the time to.
- `rounded_result` (bool, optional): If True, the result will be rounded. Defaults to True.
- `humanized_input` (bool, optional): If True, unit names can be entered in a human-readable format (e.g., "Decade" instead of "decade"). Defaults to False.
- `with_unit` (bool, optional): If True, the result will include the unit of measurement as a string. Defaults to False.

### Example Usage:
- Converting 10 seconds (s) to minutes (min):
    ```python
    time_converter(10, "second", "minute")
    ```
- Converting 10 seconds (s) to minutes (min) with the unit in the result:
    ```python
    time_converter(10, "second", "minute", with_unit=True)
    ```
- Converting 10 seconds with human-readable input:
    ```python
    time_converter(10, "Second", "Minute", humanized_input=True)
    ```

### Error Handling:
- If either `from_unit` or `to_unit` is not recognized (i.e., not in the supported `unit_list`), the function raises a `ValueError`.

### Dependencies:
- The script uses the `time_formulas` module from the `Metricus._formulas` package to perform the actual conversion operations.
- The `round_number` function is used for rounding results, and `humanize_input` allows for human-readable unit inputs.

"""

from typing import Union

from Metricus._formulas import time_formulas as timef
from Metricus.utilities import round_number, humanize_input

unit_list = [
    "millisecond",  
    "second",  
    "minute",  
    "hour",  
    "day",  
    "week",  
    "month",  
    "year",  
    "decade",  
    "century",  
]

def time_converter(
    time: float, from_unit: str, to_unit: str, rounded_result: bool = True, humanized_input: bool = False, with_unit: bool = False
) -> Union[float, str]:
    """
    Converts a given time from one unit to another.

    Args:
        time (float): The time to be converted.
        from_unit (str): The unit of the time to convert from.
        to_unit (str): The unit to convert the time to.
        rounded_result (bool, optional): If True, rounds the result. Defaults to True.
        humanized_input (bool, optional): If True, allows human-readable unit input. Defaults to False.
        with_unit (bool, optional): If True, includes the unit of measurement in the result. Defaults to False.

    Returns:
        Union[float, str]: The converted time. If `with_unit` is True, the result will include the unit as a string,
                           otherwise, it will return the numeric value of the converted time.

    Raises:
        ValueError: If either `from_unit` or `to_unit` is not recognized (not in `unit_list`).

    The function uses the `time_formulas` module from the `Metricus._formulas` package to handle the actual conversions.
    The conversion process is determined based on the `from_unit` and `to_unit` parameters.

    Example usage:
        time_converter(10, "second", "minute")  # Converts 10 seconds to minutes
        time_converter(10, "second", "minute", with_unit=True)  # Converts 10 seconds to minutes and includes the unit in the result
    """

    if humanized_input:
        from_unit = humanize_input(from_unit)
        to_unit = humanize_input(to_unit)

    if from_unit not in unit_list or to_unit not in unit_list:
        raise ValueError("The measurement has an unknown unit")

    # Conversion logic based on the 'from_unit'
    if from_unit == to_unit:
        result = round_number(time) if rounded_result else time
    elif from_unit == "millisecond":
        result = timef.Millisecond(time, with_unit=with_unit).millisecond_to(to_unit)
    elif from_unit == "second":
        result = timef.Second(time, with_unit=with_unit).second_to(to_unit)
    elif from_unit == "minute":
        result = timef.Minute(time, with_unit=with_unit).minute_to(to_unit)
    elif from_unit == "hour":
        result = timef.Hour(time, with_unit=with_unit).hour_to(to_unit)
    elif from_unit == "day":
        result = timef.Day(time, with_unit=with_unit).day_to(to_unit)
    elif from_unit == "week":
        result = timef.Week(time, with_unit=with_unit).week_to(to_unit)
    elif from_unit == "month":
        result = timef.Month(time, with_unit=with_unit).month_to(to_unit)
    elif from_unit == "year":
        result = timef.Year(time, with_unit=with_unit).year_to(to_unit)
    elif from_unit == "decade":
        result = timef.Decade(time, with_unit=with_unit).decade_to(to_unit)
    elif from_unit == "century":
        result = timef.Century(time, with_unit=with_unit).century_to(to_unit)
    else:
        raise ValueError("The measurement has an unknown unit")
    
    return round_number(result) if rounded_result else result
