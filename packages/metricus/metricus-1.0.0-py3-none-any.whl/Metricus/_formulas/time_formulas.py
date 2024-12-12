"""
This module provides classes for converting time between different units.

Classes:

    - TimeUnit: A base class for time conversions. It handles the time value and whether or not the unit should be included in the output.
    - Millisecond: A class for converting time from milliseconds (ms) to other units such as seconds (sec), minutes (min), hours (h), days (d), weeks (wk), months (mo), years (yr), decades (dec), and centuries (cent).
    - Second: A class for converting time from seconds (sec) to other units such as milliseconds (ms), minutes (min), hours (h), days (d), weeks (wk), months (mo), years (yr), decades (dec), and centuries (cent).
    - Minute: A class for converting time from minutes (min) to other units such as milliseconds (ms), seconds (sec), hours (h), days (d), weeks (wk), months (mo), years (yr), decades (dec), and centuries (cent).
    - Hour: A class for converting time from hours (h) to other units such as milliseconds (ms), seconds (sec), minutes (min), days (d), weeks (wk), months (mo), years (yr), decades (dec), and centuries (cent).
    - Day: A class for converting time from days (d) to other units such as milliseconds (ms), seconds (sec), minutes (min), hours (h), weeks (wk), months (mo), years (yr), decades (dec), and centuries (cent).
    - Week: A class for converting time from weeks (wk) to other units such as milliseconds (ms), seconds (sec), minutes (min), hours (h), days (d), months (mo), years (yr), decades (dec), and centuries (cent).
    - Month: A class for converting time from months (mo) to other units such as milliseconds (ms), seconds (sec), minutes (min), hours (h), days (d), weeks (wk), years (yr), decades (dec), and centuries (cent).
    - Year: A class for converting time from years (yr) to other units such as milliseconds (ms), seconds (sec), minutes (min), hours (h), days (d), weeks (wk), months (mo), decades (dec), and centuries (cent).
    - Decade: A class for converting time from decades (dec) to other units such as milliseconds (ms), seconds (sec), minutes (min), hours (h), days (d), weeks (wk), months (mo), years (yr), and centuries (cent).
    - Century: A class for converting time from centuries (cent) to other units such as milliseconds (ms), seconds (sec), minutes (min), hours (h), days (d), weeks (wk), months (mo), years (yr), and decades (dec).

Usage Example:

    # Create a Millisecond object
    time_ms = Millisecond(1000, with_unit=True)

    # Convert 1000 milliseconds to seconds
    result = time_ms.millisecond_to('second')
    print(result)  # Output: "1.0 sec"

    # Create a Second object
    time_sec = Second(60, with_unit=True)

    # Convert 60 seconds to minutes
    result = time_sec.second_to('minute')
    print(result)  # Output: "1.0 min"

    # Create a Minute object
    time_min = Minute(120, with_unit=True)

    # Convert 120 minutes to hours
    result = time_min.minute_to('hour')
    print(result)  # Output: "2.0 h"

    # Create an Hour object
    time_hr = Hour(48, with_unit=True)

    # Convert 48 hours to days
    result = time_hr.hour_to('day')
    print(result)  # Output: "2.0 d"

    # Create a Day object
    time_day = Day(7, with_unit=True)

    # Convert 7 days to weeks
    result = time_day.day_to('week')
    print(result)  # Output: "1.0 wk"

    # Create a Week object
    time_wk = Week(4, with_unit=True)

    # Convert 4 weeks to months
    result = time_wk.week_to('month')
    print(result)  # Output: "0.92 mo"

    # Create a Month object
    time_mo = Month(12, with_unit=True)

    # Convert 12 months to years
    result = time_mo.month_to('year')
    print(result)  # Output: "1.0 yr"

    # Create a Year object
    time_yr = Year(10, with_unit=True)

    # Convert 10 years to decades
    result = time_yr.year_to('decade')
    print(result)  # Output: "1.0 dec"

    # Create a Decade object
    time_dec = Decade(2, with_unit=True)

    # Convert 2 decades to centuries
    result = time_dec.decade_to('century')
    print(result)  # Output: "0.2 cent"

    # Create a Century object
    time_cent = Century(1, with_unit=True)

    # Convert 1 century to years
    result = time_cent.century_to('year')
    print(result)  # Output: "100 yr"
"""

from typing import Union


# Base class for Time Units
class TimeUnit:
    """
    A base class for representing and converting time units.

    Attributes:
    -----------
    num : float
        The numerical value of the time unit.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `TimeUnit` instance with a numerical value and an optional flag for including units in the result.
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
            The numerical result of the time conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        units_map = {
            "millisecond": "ms",
            "second": "sec",
            "minute": "min",
            "hour": "h",
            "day": "d",
            "week": "wk",
            "month": "mo",
            "year": "yr",
            "decade": "dec",
            "century": "cent",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Millisecond
class Millisecond(TimeUnit):
    """
    A class for converting time from milliseconds to other units.

    Methods:
    --------
    millisecond_to(self, unit: str) -> Union[float, str]
        Converts the time from milliseconds to the specified unit.
    """

    def millisecond_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from milliseconds to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "second":
            result = self.num / 1000
        elif unit == "minute":
            result = self.num / 60000
        elif unit == "hour":
            result = self.num / 3.6e6
        elif unit == "day":
            result = self.num / 8.64e7
        elif unit == "week":
            result = self.num / 6.048e8
        elif unit == "month":
            result = self.num / 2.628e9
        elif unit == "year":
            result = self.num / 3.1536e10
        elif unit == "decade":
            result = self.num / 3.1536e11
        elif unit == "century":
            result = self.num / 3.1536e12
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Second
class Second(TimeUnit):
    """
    A class for converting time from seconds to other units.

    Methods:
    --------
    second_to(self, unit: str) -> Union[float, str]
        Converts the time from seconds to the specified unit.
    """

    def second_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from seconds to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'minute', 'hour', 'day', 'week', 'month', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 1000
        elif unit == "minute":
            result = self.num / 60
        elif unit == "hour":
            result = self.num / 3600
        elif unit == "day":
            result = self.num / 86400
        elif unit == "week":
            result = self.num / 604800
        elif unit == "month":
            result = self.num / 2.628e6
        elif unit == "year":
            result = self.num / 3.154e7
        elif unit == "decade":
            result = self.num / 3.154e8
        elif unit == "century":
            result = self.num / 3.154e9
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Minute
class Minute(TimeUnit):
    """
    A class for converting time from minutes to other units.

    Methods:
    --------
    minute_to(self, unit: str) -> Union[float, str]
        Converts the time from minutes to the specified unit.
    """

    def minute_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from minutes to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'hour', 'day', 'week', 'month', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 60000
        elif unit == "second":
            result = self.num * 60
        elif unit == "hour":
            result = self.num / 60
        elif unit == "day":
            result = self.num / 1440
        elif unit == "week":
            result = self.num / 10080
        elif unit == "month":
            result = self.num / 43800
        elif unit == "year":
            result = self.num / 525600
        elif unit == "decade":
            result = self.num / 5.256e6
        elif unit == "century":
            result = self.num / 5.256e7
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Hour
class Hour(TimeUnit):
    """
    A class for converting time from hours to other units.

    Methods:
    --------
    hour_to(self, unit: str) -> Union[float, str]
        Converts the time from hours to the specified unit.
    """

    def hour_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from hours to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'day', 'week', 'month', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 3.6e6
        elif unit == "second":
            result = self.num * 3600
        elif unit == "minute":
            result = self.num * 60
        elif unit == "day":
            result = self.num / 24
        elif unit == "week":
            result = self.num / 168
        elif unit == "month":
            result = self.num / 730
        elif unit == "year":
            result = self.num / 8760
        elif unit == "decade":
            result = self.num / 87600
        elif unit == "century":
            result = self.num / 876000
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Day
class Day(TimeUnit):
    """
    A class for converting time from days to other units.

    Methods:
    --------
    day_to(self, unit: str) -> Union[float, str]
        Converts the time from days to the specified unit.
    """

    def day_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from days to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'hour', 'week', 'month', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 86400000
        elif unit == "second":
            result = self.num * 86400
        elif unit == "minute":
            result = self.num * 1440
        elif unit == "hour":
            result = self.num * 24
        elif unit == "week":
            result = self.num / 7
        elif unit == "month":
            result = self.num / 30.44
        elif unit == "year":
            result = self.num / 365.25
        elif unit == "decade":
            result = self.num / 3652.5
        elif unit == "century":
            result = self.num / 36525
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Week
class Week(TimeUnit):
    """
    A class for converting time from weeks to other units.

    Methods:
    --------
    week_to(self, unit: str) -> Union[float, str]
        Converts the time from weeks to the specified unit.
    """

    def week_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from weeks to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'hour', 'day', 'month', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 604800000
        elif unit == "second":
            result = self.num * 604800
        elif unit == "minute":
            result = self.num * 10080
        elif unit == "hour":
            result = self.num * 168
        elif unit == "day":
            result = self.num * 7
        elif unit == "month":
            result = self.num / 4.348
        elif unit == "year":
            result = self.num / 52.1786
        elif unit == "decade":
            result = self.num / 521.786
        elif unit == "century":
            result = self.num / 5217.86
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Month
class Month(TimeUnit):
    """
    A class for converting time from months to other units.

    Methods:
    --------
    month_to(self, unit: str) -> Union[float, str]
        Converts the time from months to the specified unit.
    """

    def month_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from months to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'year', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 2.628e9
        elif unit == "second":
            result = self.num * 2.628e6
        elif unit == "minute":
            result = self.num * 43800
        elif unit == "hour":
            result = self.num * 730
        elif unit == "day":
            result = self.num * 30.44
        elif unit == "week":
            result = self.num * 4.348
        elif unit == "year":
            result = self.num / 12
        elif unit == "decade":
            result = self.num / 120
        elif unit == "century":
            result = self.num / 1200
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Year
class Year(TimeUnit):
    """
    A class for converting time from years to other units.

    Methods:
    --------
    year_to(self, unit: str) -> Union[float, str]
        Converts the time from years to the specified unit.
    """

    def year_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from years to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'decade', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 3.154e10
        elif unit == "second":
            result = self.num * 3.154e7
        elif unit == "minute":
            result = self.num * 525600
        elif unit == "hour":
            result = self.num * 8760
        elif unit == "day":
            result = self.num * 365.25
        elif unit == "week":
            result = self.num * 52.1786
        elif unit == "month":
            result = self.num * 12
        elif unit == "decade":
            result = self.num / 10
        elif unit == "century":
            result = self.num / 100
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Decade
class Decade(TimeUnit):
    """
    A class for converting time from decades to other units.

    Methods:
    --------
    decade_to(self, unit: str) -> Union[float, str]
        Converts the time from decades to the specified unit.
    """

    def decade_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from decades to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', and 'century'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 3.154e11
        elif unit == "second":
            result = self.num * 3.154e8
        elif unit == "minute":
            result = self.num * 5.256e6
        elif unit == "hour":
            result = self.num * 87600
        elif unit == "day":
            result = self.num * 3652.5
        elif unit == "week":
            result = self.num * 521.786
        elif unit == "month":
            result = self.num * 120
        elif unit == "year":
            result = self.num * 10
        elif unit == "century":
            result = self.num / 10
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)


# Century
class Century(TimeUnit):
    """
    A class for converting time from centuries to other units.

    Methods:
    --------
    century_to(self, unit: str) -> Union[float, str]
        Converts the time from centuries to the specified unit.
    """

    def century_to(self, unit: str) -> Union[float, str]:
        """
        Converts the time from centuries to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', and 'decade'.

        Returns:
        --------
        Union[float, str]
            The converted time value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If an invalid unit is provided.
        """
        if unit == "millisecond":
            result = self.num * 3.154e12
        elif unit == "second":
            result = self.num * 3.154e9
        elif unit == "minute":
            result = self.num * 5.256e7
        elif unit == "hour":
            result = self.num * 876000
        elif unit == "day":
            result = self.num * 36525
        elif unit == "week":
            result = self.num * 5217.86
        elif unit == "month":
            result = self.num * 1200
        elif unit == "year":
            result = self.num * 100
        elif unit == "decade":
            result = self.num * 10
        else:
            raise ValueError("The measurement has an unknown unit")

        return self.format_result(result, unit)
