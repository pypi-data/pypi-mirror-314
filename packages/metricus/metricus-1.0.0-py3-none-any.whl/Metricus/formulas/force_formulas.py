"""
This module provides classes for converting force between different units.

Classes:
    - Force: A base class for force conversions. It handles the force value and whether or not the unit should be included in the output.
    - Newton: A class for converting force from Newtons (N) to other units such as Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - Dyne: A class for converting force from Dyne (dyn) to other units such as Newton (N), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - Kilonewton: A class for converting force from Kilonewton (kN) to other units such as Newton (N), Dyne (dyn), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - PoundForce: A class for converting force from Pound Force (lbf) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - OunceForce: A class for converting force from Ounce Force (ozf) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - TonForce: A class for converting force from Ton Force (tnf) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - KilogramForce: A class for converting force from Kilogram Force (kgf) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Gram Force (gf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - GramForce: A class for converting force from Gram Force (gf) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Millinewton (mN), Poundal (pdl), and Slug Force (slf).
    - Millinewton: A class for converting force from Millinewton (mN) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Poundal (pdl), and Slug Force (slf).
    - Poundal: A class for converting force from Poundal (pdl) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), and Slug Force (slf).
    - SlugForce: A class for converting force from Slug Force (slf) to other units such as Newton (N), Dyne (dyn), Kilonewton (kN), Pound Force (lbf), Ounce Force (ozf), Ton Force (tnf), Kilogram Force (kgf), Gram Force (gf), Millinewton (mN), Poundal (pdl).

Usage Example:
    # Create a Newton object
    force_n = Newton(10, with_unit=True)
    # Convert 10 N to kilogram force (kgf)
    result = force_n.newton_to('kilogram_force')
    print(result)  # Output: "1.019716 kgf"

    # Create a Dyne object
    force_dyn = Dyne(100000, with_unit=False)
    # Convert 100000 dyn to newtons (N)
    result = force_dyn.dyne_to('newton')
    print(result)  # Output: 1.0

    # Create a Kilonewton object
    force_kn = Kilonewton(5, with_unit=True)
    # Convert 5 kN to pound force (lbf)
    result = force_kn.kilonewton_to('pound_force')
    print(result)  # Output: "1124.045 lbf"

    # Create a PoundForce object
    force_lbf = PoundForce(20, with_unit=False)
    # Convert 20 lbf to ton force (tnf)
    result = force_lbf.pound_force_to('ton_force')
    print(result)  # Output: 0.008896

    # Create a Poundal object
    force_pdl = Poundal(100, with_unit=True)
    # Convert 100 pdl to newtons (N)
    result = force_pdl.poundal_to('newton')
    print(result)  # Output: "445.564 N"

    # Create a SlugForce object
    force_slf = SlugForce(50, with_unit=True)
    # Convert 50 slf to newtons (N)
    result = force_slf.slug_force_to('newton')
    print(result)  # Output: "1605.287 N"
"""

from typing import Union


# Base class for force units
class Force:
    """
    A base class for representing and converting forces.

    Attributes:
    -----------
    num : float
        The numerical value of the force.
    with_unit : bool
        Indicates whether the result should include the unit (default is False).

    Methods:
    --------
    __init__(self, num: float, with_unit: bool = False) -> None
        Initializes the `Force` instance with a numerical value and an optional flag for including units in the result.
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
            The numerical result of the force conversion.
        unit : str
            The unit to include in the formatted result.

        Returns:
        --------
        Union[float, str]
            The formatted result with or without the unit.
        """
        units_map = {
            "newton": "N",
            "dyne": "dyn",
            "kilonewton": "kN",
            "pound_force": "lbf",
            "ounce_force": "ozf",
            "ton_force": "tnf",
            "kilogram_force": "kgf",
            "gram_force": "gf",
            "millinewton": "mN",
            "poundal": "pdl",
            "slug_force": "slf",
        }
        return f"{result} {units_map[unit]}" if self.with_unit else result


# Newton
class Newton(Force):
    """
    A class for converting force from Newton (N) to other units.

    Methods:
    --------
    newton_to(self, unit: str) -> Union[float, str]
        Converts force from Newton to the specified unit.
    """

    def newton_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Newton to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'dyne', 'kilonewton', 'pound_force', 'ounce_force',
            'ton_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "dyne":
            result = self.num * 10**5
        elif unit == "kilonewton":
            result = self.num / 1000
        elif unit == "pound_force":
            result = self.num * 0.224809
        elif unit == "ounce_force":
            result = self.num * 35.27396
        elif unit == "ton_force":
            result = self.num * 9.8196e-5
        elif unit == "kilogram_force":
            result = self.num * 0.1019716
        elif unit == "gram_force":
            result = self.num * 101.9716
        elif unit == "millinewton":
            result = self.num * 1000
        elif unit == "poundal":
            result = self.num * 0.007375
        elif unit == "slug_force":
            result = self.num * 0.031081
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Dyne
class Dyne(Force):
    """
    A class for converting force from Dyne (dyn) to other units.

    Methods:
    --------
    dyne_to(self, unit: str) -> Union[float, str]
        Converts force from Dyne to the specified unit.
    """

    def dyne_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Dyne to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'kilonewton', 'pound_force', 'ounce_force',
            'ton_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 10**5
        elif unit == "kilonewton":
            result = self.num / 10**8
        elif unit == "pound_force":
            result = self.num * 2.248e-6
        elif unit == "ounce_force":
            result = self.num * 3.527396e-5
        elif unit == "ton_force":
            result = self.num * 9.8196e-10
        elif unit == "kilogram_force":
            result = self.num * 1.019716e-7
        elif unit == "gram_force":
            result = self.num * 1.019716e-4
        elif unit == "millinewton":
            result = self.num * 0.01
        elif unit == "poundal":
            result = self.num * 7.375e-8
        elif unit == "slug_force":
            result = self.num * 3.1081e-7
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Kilonewton
class Kilonewton(Force):
    """
    A class for converting force from Kilonewton (kN) to other units.

    Methods:
    --------
    kilonewton_to(self, unit: str) -> Union[float, str]
        Converts force from Kilonewton to the specified unit.
    """

    def kilonewton_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Kilonewton to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'pound_force', 'ounce_force',
            'ton_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num * 1000
        elif unit == "dyne":
            result = self.num * 10**8
        elif unit == "pound_force":
            result = self.num * 224.809
        elif unit == "ounce_force":
            result = self.num * 35273.96
        elif unit == "ton_force":
            result = self.num * 0.098196
        elif unit == "kilogram_force":
            result = self.num * 101.9716
        elif unit == "gram_force":
            result = self.num * 101971.6
        elif unit == "millinewton":
            result = self.num * 1e6
        elif unit == "poundal":
            result = self.num * 7.375
        elif unit == "slug_force":
            result = self.num * 31.081
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Pound Force
class PoundForce(Force):
    """
    A class for converting force from Pound Force (lbf) to other units.

    Methods:
    --------
    pound_force_to(self, unit: str) -> Union[float, str]
        Converts force from Pound Force to the specified unit.
    """

    def pound_force_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Pound Force to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'ounce_force',
            'ton_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 0.224809
        elif unit == "dyne":
            result = self.num * 4.4482e4
        elif unit == "kilonewton":
            result = self.num / 224.809
        elif unit == "ounce_force":
            result = self.num * 16
        elif unit == "ton_force":
            result = self.num * 4.4482e-4
        elif unit == "kilogram_force":
            result = self.num * 0.453592
        elif unit == "gram_force":
            result = self.num * 453.592
        elif unit == "millinewton":
            result = self.num * 4448.22
        elif unit == "poundal":
            result = self.num * 32.174
        elif unit == "slug_force":
            result = self.num * 1.35582
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Ounce Force
class OunceForce(Force):
    """
    A class for converting force from Ounce Force (ozf) to other units.

    Methods:
    --------
    ounce_force_to(self, unit: str) -> Union[float, str]
        Converts force from Ounce Force to the specified unit.
    """

    def ounce_force_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Ounce Force to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ton_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 35.27396
        elif unit == "dyne":
            result = self.num * 280.2265
        elif unit == "kilonewton":
            result = self.num / 35273.96
        elif unit == "pound_force":
            result = self.num / 16
        elif unit == "ton_force":
            result = self.num * 2.836e-5
        elif unit == "kilogram_force":
            result = self.num * 0.0283495
        elif unit == "gram_force":
            result = self.num * 28.3495
        elif unit == "millinewton":
            result = self.num * 28349.5
        elif unit == "poundal":
            result = self.num * 2.0109
        elif unit == "slug_force":
            result = self.num * 0.084732
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Ton Force
class TonForce(Force):
    """
    A class for converting force from Ton Force (tnf) to other units.

    Methods:
    --------
    ton_force_to(self, unit: str) -> Union[float, str]
        Converts force from Ton Force to the specified unit.
    """

    def ton_force_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Ton Force to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ounce_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 9.8196e-5
        elif unit == "dyne":
            result = self.num * 1.019716e7
        elif unit == "kilonewton":
            result = self.num / 9.8196
        elif unit == "pound_force":
            result = self.num * 2248.09
        elif unit == "ounce_force":
            result = self.num * 3.527396e4
        elif unit == "kilogram_force":
            result = self.num * 1019.716
        elif unit == "gram_force":
            result = self.num * 1.019716e6
        elif unit == "millinewton":
            result = self.num * 9.8196e7
        elif unit == "poundal":
            result = self.num * 7375.08
        elif unit == "slug_force":
            result = self.num * 3108.1
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Kilogram Force
class KilogramForce(Force):
    """
    A class for converting force from Kilogram Force (kgf) to other units.

    Methods:
    --------
    kilogram_force_to(self, unit: str) -> Union[float, str]
        Converts force from Kilogram Force to the specified unit.
    """

    def kilogram_force_to(self, unit: str) -> Union[float, str]:
        """
        Converts force from Kilogram Force to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ounce_force', 'ton_force', 'gram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num * 9.81
        elif unit == "dyne":
            result = self.num * 9.81e5
        elif unit == "kilonewton":
            result = self.num / 1000
        elif unit == "pound_force":
            result = self.num * 2.204623
        elif unit == "ounce_force":
            result = self.num * 35.27396
        elif unit == "ton_force":
            result = self.num / 1019.716
        elif unit == "gram_force":
            result = self.num * 1000
        elif unit == "millinewton":
            result = self.num * 9806.65
        elif unit == "poundal":
            result = self.num * 7.375
        elif unit == "slug_force":
            result = self.num * 0.031081
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Gram Force
class GramForce(Force):
    """
    A class for converting Gram Force (gf) to other units of force.

    Methods:
    --------
    gram_force_to(self, unit: str) -> Union[float, str]
        Converts Gram Force to the specified unit.
    """

    def gram_force_to(self, unit: str) -> Union[float, str]:
        """
        Converts Gram Force (gf) to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ounce_force', 'ton_force', 'kilogram_force', 'millinewton', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num * 9.81e-3
        elif unit == "dyne":
            result = self.num * 981
        elif unit == "kilonewton":
            result = self.num / 1e6
        elif unit == "pound_force":
            result = self.num * 2.2046e-3
        elif unit == "ounce_force":
            result = self.num * 3.527396e-2
        elif unit == "ton_force":
            result = self.num / 1.019716e6
        elif unit == "kilogram_force":
            result = self.num / 1000
        elif unit == "millinewton":
            result = self.num * 9.81
        elif unit == "poundal":
            result = self.num * 7.375e-3
        elif unit == "slug_force":
            result = self.num * 3.1081e-5
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Millinewton
class Millinewton(Force):
    """
    A class for converting Millinewton (mN) to other units of force.

    Methods:
    --------
    millinewton_to(self, unit: str) -> Union[float, str]
        Converts Millinewton to the specified unit.
    """

    def millinewton_to(self, unit: str) -> Union[float, str]:
        """
        Converts Millinewton (mN) to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ounce_force', 'ton_force', 'kilogram_force', 'gram_force', 'poundal', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 1000
        elif unit == "dyne":
            result = self.num * 10
        elif unit == "kilonewton":
            result = self.num / 1e6
        elif unit == "pound_force":
            result = self.num * 2.248e-6
        elif unit == "ounce_force":
            result = self.num * 3.527396e-5
        elif unit == "ton_force":
            result = self.num / 9.8196e7
        elif unit == "kilogram_force":
            result = self.num / 9806.65
        elif unit == "gram_force":
            result = self.num / 9.81
        elif unit == "poundal":
            result = self.num * 7.375e-6
        elif unit == "slug_force":
            result = self.num * 3.1081e-5
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# Poundal
class Poundal(Force):
    """
    A class for converting Poundal (pdl) to other units of force.

    Methods:
    --------
    poundal_to(self, unit: str) -> Union[float, str]
        Converts Poundal to the specified unit.
    """

    def poundal_to(self, unit: str) -> Union[float, str]:
        """
        Converts Poundal (pdl) to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ounce_force', 'ton_force', 'kilogram_force', 'gram_force', 'millinewton', and 'slug_force'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 0.224809
        elif unit == "dyne":
            result = self.num * 144.864
        elif unit == "kilonewton":
            result = self.num / 224.809
        elif unit == "pound_force":
            result = self.num / 32.174
        elif unit == "ounce_force":
            result = self.num / 2.0109
        elif unit == "ton_force":
            result = self.num / 7375.08
        elif unit == "kilogram_force":
            result = self.num / 7.375
        elif unit == "gram_force":
            result = self.num * 0.07375
        elif unit == "millinewton":
            result = self.num * 137.374
        elif unit == "slug_force":
            result = self.num * 0.045
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)


# SlugForce
class SlugForce(Force):
    """
    A class for converting Slug Force (slf) to other units of force.

    Methods:
    --------
    slug_force_to(self, unit: str) -> Union[float, str]
        Converts Slug Force to the specified unit.
    """

    def slug_force_to(self, unit: str) -> Union[float, str]:
        """
        Converts Slug Force (slf) to the specified unit.

        Parameters:
        -----------
        unit : str
            The unit to convert to. Supported units are 'newton', 'dyne', 'kilonewton', 'pound_force',
            'ounce_force', 'ton_force', 'kilogram_force', 'gram_force', 'millinewton', 'poundal'.

        Returns:
        --------
        Union[float, str]
            The converted force value, formatted with unit if `with_unit` is set to `True`.

        Raises:
        -------
        ValueError
            If the provided unit is unknown.
        """
        if unit == "newton":
            result = self.num / 0.031081
        elif unit == "dyne":
            result = self.num * 3225.7
        elif unit == "kilonewton":
            result = self.num / 31.081
        elif unit == "pound_force":
            result = self.num / 1.35582
        elif unit == "ounce_force":
            result = self.num / 0.084732
        elif unit == "ton_force":
            result = self.num / 3108.1
        elif unit == "kilogram_force":
            result = self.num / 31.081
        elif unit == "gram_force":
            result = self.num * 31.081
        elif unit == "millinewton":
            result = self.num * 3.1081e3
        elif unit == "poundal":
            result = self.num / 0.045
        else:
            raise ValueError("Unknown unit")

        return self.format_result(result, unit)
