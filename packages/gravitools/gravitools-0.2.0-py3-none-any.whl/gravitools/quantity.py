from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
import re


# TODO: Allow parentheses notation
def parse_quantity(text: str | float) -> tuple(float, float, str):
    """Parse a quantity string into value, uncertainty and units

    Also accepts float values. These are simply passed through.

    Examples:
        >>> parse_quantity("12.34 ± 0.01 nm/s²")
        (12.34, 0.01, 'nm/s²')
        >>> parse_quantity(12.34)
        (12.34, None, None)
    """
    if isinstance(text, (int, float)):
        return float(text), None, None
    if not isinstance(text, str):
        raise TypeError(f"Cannot parse type {type(text)}. Expected str or number.")

    pattern = (
        r"(?P<value>[\d+\-_,.eE]+)(\s?±\s?(?P<uncert>[\d_,.eE]+))?(\s*(?P<units>\S+))?"
    )
    match = re.fullmatch(pattern, text.strip())
    if match is None:
        raise ValueError(f"Cannot parse quantity string {text!r}")
    value = float(match.group("value").replace(",", ""))
    uncert = (
        float(match.group("uncert").replace(",", "")) if match.group("uncert") else None
    )
    units = match.group("units")
    return value, uncert, units


def parse_pressure_admittance(text: str | float) -> float:
    """Parse a pressure admittance string

    Args:
        text:
            If the input is a number, it is assumed to be in units of
            nm/s²/hPa.

    Returns:
        Pressure admittance value.

    Examples:
        >>> parse_pressure_admittance("-3 nm/s²/hPa")
        -3.0
        >>> parse_pressure_admittance("-0.3 µGal/hPa")
        -3.0
        >>> parse_pressure_admittance(-3)
        -3.0
    """
    value, uncert, units = parse_quantity(text)
    if uncert:
        raise NotImplementedError(text)
    if not units:
        units = "nm/s²/hPa"
    if value >= 0:
        raise ValueError(f"Admittance factor should be negative, but is {text}")
    if units == "µGal/hPa":
        return value * 10
    if units in ["nm/s²/hPa", "nm/s^2/hPa"]:
        return value
    raise ValueError(f"Unknown units: {units}")


def format_pressure_admittance(value: float) -> str:
    """Format a pressure admittance value"""
    return f"{value:.2f} nm/s²/hPa"


def clean_pressure_admittance(text: str | float) -> str:
    """Parse a pressure admittance string and format in standard form

    Examples:
        >>> clean_pressure_admittance('-0.3 µGal/hPa')
        '-3.00 nm/s²/hPa'
    """
    return format_pressure_admittance(parse_pressure_admittance(text))


def parse_height(text: str | float) -> float:
    """Parse a height string

    If no units are specified, value is interpreted as meters. This is for
    compatibility with very early AQG metadata files.

    Examples:
        >>> parse_height("123.45 m")
        123.45
        >>> parse_height("123.45")
        123.45
    """
    value, uncert, units = parse_quantity(text)
    if uncert:
        raise NotImplementedError(text)
    if not units:
        units = "m"
    if units == "m":
        return value
    raise ValueError(f"Unknown units: {units}")


def format_height(value: float) -> str:
    """Format a height value"""
    return f"{value:.4f} m"


def clean_height(text: str) -> str:
    """Parse a height value string and format in standard form

    Examples:
        >>> clean_height('1.25')
        '1.2500 m'
    """
    return format_height(parse_height(text))


def parse_coord_angle(text: str | float) -> float:
    """Parse a latitude or longitude angle string

    Examples:
        >>> parse_coord_angle("12.4567 °")
        12.4567
        >>> parse_coord_angle("12.4567°")
        12.4567
    """
    value, uncert, units = parse_quantity(text)
    if uncert:
        raise NotImplementedError(text)
    if not units:
        units = "°"
    if units == "°":
        return value
    raise ValueError(f"Unknown units: {units}")


def format_coord_angle(value: float) -> str:
    """Format a coordinate angle value"""
    return f"{value:.6f}°"


def clean_coord_angle(text: str) -> str:
    """Parse a coordinate angle and format in standard form

    Examples:
        >>> clean_coord_angle('12.34°')
        '12.340000°'
    """
    return format_coord_angle(parse_coord_angle(text))


def parse_tilt_angle(text: str | float) -> float:
    """
    Parse an instrument tilt angle

    Examples:
        >>> parse_tilt_angle("1e-6 rad")
        1e-06
        >>> parse_tilt_angle("0.001 mrad")
        1e-06
        >>> parse_tilt_angle("1 µrad")
        1e-06
        >>> parse_tilt_angle(1e-6)
        1e-06
    """
    value, uncert, units = parse_quantity(text)
    if uncert:
        raise NotImplementedError(text)
    if not units:
        units = "rad"
    if units == "rad":
        return value
    if units == "mrad":
        return value * 1e-3
    if units in ["µrad", "urad"]:
        return value * 1e-6
    raise ValueError(f"Unknown units: {units!r}")


def format_tilt_angle(value: float) -> str:
    return f"{value * 1e6:.1f}e-6 rad"


def clean_tilt_angle(text: str) -> str:
    return format_tilt_angle(parse_tilt_angle(text))


def parse_orientation(text: str | float) -> str:
    return parse_coord_angle(text)


def format_orientation(value: float) -> str:
    return f"{value:.1f}°"


def clean_orientation(text: str | float) -> str:
    return format_orientation(parse_orientation(text))


@dataclass
class GValue:
    """A relative gravity value

    Provides arithmetic, string formatting and error propagation (sum of squares).

    Examples:
        >>> GValue(100, 10) + GValue(200, 10)
        GValue(value=300, error=14.142135623730951)

        >>> 10 * GValue(100, 10)
        GValue(value=1000, error=100)

        >>> str(GValue(123.456))
        '123.5 nm/s²'

        >>> str(GValue(123.456, 12.34))
        '123.5 ± 12.3 nm/s²'
    """

    value: float
    """Gravity value, in nm/s²"""
    error: float = 0
    """Standard error, in nm/s²"""

    def __post_init__(self):
        if self.error < 0:
            raise ValueError("Error value cannot be negative")

    def __str__(self):
        if self.error:
            return f"{self.value:,.1f} ± {self.error:,.1f} nm/s²"
        return f"{self.value:,.1f} nm/s²"

    def __float__(self):
        return float(self.value)

    def __add__(self, other):
        if hasattr(other, "value") and hasattr(other, "error"):
            # Error propagation
            return GValue(
                self.value + other.value, sqrt(self.error**2 + other.error**2)
            )
        return GValue(self.value + other, self.error)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-1 * other)

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, other):
        return GValue(self.value * other, abs(self.error * other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return -1 * self

    @classmethod
    def from_str(cls, text: str | float):
        """Parse a gravity value string

        Examples:
            >>> GValue.from_str("123.4 nm/s²")
            GValue(value=123.4, error=0)
            >>> GValue.from_str("12.34 µGal")
            GValue(value=123.4, error=0)
            >>> GValue.from_str("123.4 ± 1.2 nm/s²")
            GValue(value=123.4, error=1.2)
        """
        value, uncert, units = parse_quantity(text)
        if uncert is None:
            uncert = 0
        if units is None:
            units = "nm/s²"
        if units == "µGal":
            # Convert to nm/s²
            value *= 10
            uncert *= 10
        elif units not in ["nm/s²", "nm/s^2"]:
            raise ValueError(f"Unknown units: '{units}'")
        return cls(value, uncert)

    def as_tuple(self):
        """Convert to a tuple of value and error"""
        return self.value, self.error

    @property
    def only_value(self):
        return self.__class__(self.value)


def parse_gravity(value: str | float) -> GValue:
    """Parse a gravity float value or string"""
    return GValue.from_str(value)


def clean_gravity(value: str | float) -> str:
    """Bring gravity value string to standard form

    Examples:
        >>> clean_gravity('12.34 µGal')
        '123.4 nm/s²'
        >>> clean_gravity(123.4)
        '123.4 nm/s²'
    """
    return str(parse_gravity(value))


@dataclass
class Gradient:
    """Vertical gravity gradient

    Examples:
        >>> str(Gradient(-3000))
        '-3000.0 nm/s²/m'

        >>> str(Gradient(-3000, 10))
        '-3000.0 ± 10.0 nm/s²/m'
    """

    value: float
    """Vertical gravity gradient, in nm s^-2^ m^-1^"""
    error: float = 0
    """Standard error, in nm s^-2^ m^-1^"""

    def __post_init__(self):
        if self.value > 0:
            raise ValueError(f"Gradient should be negative, but is {self.value!r}")
        if self.error < 0:
            raise ValueError(f"Error value cannot be negative, but is {self.error!r}")

    def __str__(self):
        s = f"{self.value:.1f}"
        if self.error:
            s += f" ± {self.error:.1f}"
        return s + " nm/s²/m"

    def __float__(self):
        return float(self.value)

    @classmethod
    def from_str(cls, text):
        """Convert string to Gradient

        Examples:
            >>> Gradient.from_str("-300 µGal/m")
            Gradient(value=-3000.0, error=0)

            >>> Gradient.from_str("-3000 nm/s²/m")
            Gradient(value=-3000.0, error=0)

            >>> Gradient.from_str("-300 µGal/m")
            Gradient(value=-3000.0, error=0)

        Args:
            text (str): Input string.
        """
        value, uncert, units = parse_quantity(text)
        if units is None:
            units = "nm/s²/m"
        if uncert is None:
            uncert = 0

        # By convention, the gradient is negative
        value = -abs(value)

        if units == "µGal/m":
            value *= 10
            uncert *= 10
        elif units not in ["nm/s²/m", "nm/s^2/m"]:
            raise ValueError(f"Unknown units: '{units}'")
        return cls(value, uncert)

    def as_tuple(self):
        """Convert to a tuple of value and error"""
        return self.value, self.error

    def dg_height(self, height_difference):
        """Gravity height transfer correction

        Args:
            height_difference (float):
                Difference to original measurement height, in meters.

        Returns:
            (GValue): Height transfer correction.
        """
        return height_difference * GValue(self.value, self.error)


def parse_gradient(value: float | str) -> Gradient:
    """Parse a gravity gradient value"""
    return Gradient.from_str(value) if isinstance(value, str) else Gradient(value)


def clean_gradient(text: str) -> str:
    """Bring gravity gradient string to standard form

    Examples:
        >>> clean_gradient('-300 µGal/m')
        '-3000.0 nm/s²/m'
    """
    return str(parse_gradient(text))


@dataclass
class AbsGValue:
    """Absolute gravity value

    Examples:
        >>> AbsGValue(9.81e9, 30, height=1.25, vgg=Gradient(-3000))\
            # doctest: +NORMALIZE_WHITESPACE
        AbsGValue(value=9810000000.0,  error=30, height=1.25,
            vgg=Gradient(value=-3000, error=0))

        >>> str(AbsGValue(9.81e9))
        '9,810,000,000.0 nm/s²'

        >>> str(AbsGValue(9.81e9, 30))
        '9,810,000,000.0 ± 30.0 nm/s²'

        >>> str(AbsGValue(9.81e9, 30, 1.25))
        '9,810,000,000.0 ± 30.0 nm/s² (1.25 m)'
    """

    value: float
    """Absolute gravity value, in nm/s²"""
    error: float = 0
    """Standard error, in nm/s²"""
    height: float = None
    """Measurement height, in m"""
    vgg: Gradient = None
    """Vertical gravity gradient used for height transfer"""

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Absolute gravity value cannot be negative")
        if self.error < 0:
            raise ValueError("Error cannot be negative")

    def __str__(self):
        err = f" ± {self.error:,.1f}" if self.error else ""
        h = f" ({self.height} m)" if self.height is not None else ""
        return f"{self.value:,.1f}{err} nm/s²{h}"

    def __float__(self):
        return float(self.value)

    def __add__(self, other):
        if hasattr(other, "height"):
            raise ValueError("Cannot add two absolute gravity values")
        g = GValue(self.value, self.error) + other
        return AbsGValue(value=g.value, error=g.error, height=self.height, vgg=self.vgg)

    def __sub__(self, other):
        if hasattr(other, "height"):
            if self.height != other.height:
                raise ValueError(
                    "Cannot subtract absolute gravity values at different heights"
                )
            # Return a relative gravity value
            return GValue(self.value, self.error) - GValue(other.value, other.error)

        # This must be a relative value, so we can subtract it and return a
        # new absolute gravity value.
        return self + (-1 * other)

    def as_gvalue(self):
        """Convert to a relative gravity value

        Examples:
            >>> AbsGValue(9.81e9, 30).as_gvalue()
            GValue(value=9810000000.0, error=30)
        """
        return GValue(self.value, error=self.error)

    @property
    def only_value(self):
        return self.__class__(self.value)

    def transfer(self, height):
        """Transfer gravity value to a different height

        Args:
            height (float): New height, in meters.

        Returns:
            (AbsGValue): Absolute gravity value at new height

        Examples:
            >>> AbsGValue(9.8e9, 30, height=1.25, vgg=Gradient(-3200, 20)).transfer(0)\
                # doctest: +NORMALIZE_WHITESPACE
            AbsGValue(value=9800004000.0, error=39.05124837953327, height=0,
                vgg=Gradient(value=-3200, error=20))
        """
        if self.vgg is None:
            raise ValueError("Gravity gradient is missing")
        if self.height is None:
            raise ValueError("Height is missing")
        g = self.as_gvalue() + self.vgg.dg_height(height - self.height)
        return AbsGValue(g.value, g.error, height, self.vgg)
