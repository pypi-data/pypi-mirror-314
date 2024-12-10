"""
Corrections to a gravity signal

Sign of corrections:
    All corrections have to be *subtracted* from the measured gravity value.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from gravitools.utils import interpolate_time_series

logger = logging.getLogger(__name__)


STANDARD_ADMITTANCE = -3
"""Standard pressure admittance factor, in nm/s² per hPa"""

EOP_URL = "https://datacenter.iers.org/data/csv/finals2000A.all.csv"
"""Default URL to EOP data"""

EOP_PATH = Path.home() / ".config" / "gravitools" / "finals2000A.all.csv"
"""Default path where EOP data is saved"""

# Singleton
eop_data = None
"""Earth orientation parameter data

This is set automatically by `read_eop_data()`.
"""


def read_eop_data(path=None):
    """Read EOP data from file"""
    path = path or EOP_PATH
    logger.info(f"Read EOP data from {path}")
    global eop_data
    eop_data = pd.read_csv(path, sep=";")
    eop_data.index = pd.to_datetime(eop_data[["Year", "Month", "Day"]], utc=True)
    eop_data.index.name = "utc"
    eop_data = (
        eop_data[["x_pole", "y_pole", "Type"]]
        .dropna()
        .rename(columns={"x_pole": "x", "y_pole": "y", "Type": "type"})
    )
    return eop_data


def get_eop_data():
    """Read the EOP data from file, if it is not yet available"""
    global eop_data
    if eop_data is None:
        return read_eop_data()
    return eop_data


def _download_file(url, path=None):
    """Download a file and save it to disk"""
    path = Path(path or Path(url).name)
    logger.info(f"Save {url} to {path}")
    try:
        req = requests.get(url, timeout=5)
        req.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise ValueError(f"Could not download {url}") from exc
    path.write_bytes(req.content)
    return path


def update_eop_data(expire="12h"):
    """Request the EOP data file, if necessary"""
    path = EOP_PATH
    age = (
        (pd.Timestamp.utcnow() - pd.Timestamp(path.stat().st_mtime, unit="s", tz="utc"))
        if path.exists()
        else None
    )
    if age is None or age > pd.Timedelta(expire):
        path.parent.mkdir(parents=True, exist_ok=True)
        _download_file(EOP_URL, path)
    return read_eop_data(path)


def nominal_pressure(altitude: float) -> float:
    """Nominal pressure at given altitude.

    Args:
        altitude: Location altitude, in meters.

    Returns:
        Nominal pressure, in hPa.
    """
    return 1013.25 * (1 - 0.0065 * altitude / 288.15) ** 5.2559


def pressure_correction(
    p_atm: float | pd.Series | np.ndarray,
    altitude: float,
    admittance: float = STANDARD_ADMITTANCE,
) -> float | pd.Series | np.ndarray:
    """Gravity correction due to atmospheric pressure.

    Args:
        p_atm: Atmospheric pressure values, in hPa.
        altitude: Location altitude, in meters.
        admittance: Pressure admittance factor, in nm/s^2 per hPa.

    Returns:
        Gravity correction, in nm/s².
    """
    return admittance * (p_atm - nominal_pressure(altitude))


def effective_tilt(tilt_x: np.ndarray, tilt_y: np.ndarray) -> np.ndarray:
    """Effective tilt angle, from X and Y angles"""
    # tan²(tilt) = tan²(tilt_x) + tan²(tilt_y)
    return np.arctan(np.sqrt(np.square(np.tan(tilt_x)) + np.square(np.tan(tilt_y))))


def tilt_correction(
    g_raw: np.ndarray, tilt_x: np.ndarray, tilt_y: np.ndarray
) -> np.ndarray:
    """Instrument tilt gravity correction.

    Note  that `tilt_x` and `tilt_y` are cast to float64, because float32 is
    insufficient precision.

    Args:
        g_raw (float): Measured gravity value, in nm/s².
        tilt_x (float): Instrument tilt angle in X direction, in rad.
        tilt_y (float): Instrument tilt angle in Y direction, in rad.

    Returns:
        (float): Gravity correction, in nm/s².
    """
    tilt_x = np.asarray(tilt_x, dtype=np.float64)
    tilt_y = np.asarray(tilt_y, dtype=np.float64)
    return g_raw * (1 - 1 / np.cos(effective_tilt(tilt_x, tilt_y)))


def polar_motion_correction(pol_x, pol_y, lat, lon):
    """Gravity correction due to polar motion.

    Reference: IAGBN Absolute Gravity Observations Documentation for
    BGI-Files (1992).

    Args:
        pol_x (float): Polar motion X angle coorinate, in arcsec.
        pol_y (float): Polar motion Y angle coorinate, in arcsec.
        lat (float): Latitude of measurement site, in degree.
        lon (float): Longitude of measurement site, in degree.

    Returns:
        (float): Gravity correction, in nm/s².
    """
    # Earth angular velocity
    omega = 7.292115e-5  # rad/s

    # Earth radius
    r = 6378.137e3  # m

    # Convert polar motion coordinates from arcsec to radian
    x = pol_x / 3600 / 180 * np.pi
    y = pol_y / 3600 / 180 * np.pi

    # Convert latitude and longitude from degree to radian
    phi = lat / 180 * np.pi
    lam = lon / 180 * np.pi

    # Amplitude factor
    delta = 1.164

    delta_g = (
        2
        * delta
        * omega**2
        * r
        * np.sin(phi)
        * np.cos(phi)
        * (x * np.cos(lam) - y * np.sin(lam))
    )

    # Convert from m/s² to nm/s²
    delta_g *= 1e9

    return delta_g


def dg_polar(timeindex, lat, lon, eop=None):
    """Polar motion correction for a time series.

    Args:
        timeindex (pd.DatetimeIndex):
            Time index (UTC) for which to calculate the correction.
        lat (float): Latitude, in degree.
        lon (float): Longitude, in degree.
        eop (pd.DataFrame): Time series of polar motion coordinates.

    Returns:
        (pd.Series): Time series of polar motion correction, in nm/s².
    """

    # Query EOP data, if not given
    if eop is None:
        eop = get_eop_data()

    # Calculate correction at EOP timeindices
    dg_pm = polar_motion_correction(eop.x, eop.y, lat, lon)

    if any(eop.loc[timeindex[0] : timeindex[-1], "type"] == "prediction"):
        logger.warning("You are using EOP prediction data.")

    # Linearly interpolate to given timeindex
    y = interpolate_time_series(dg_pm, timeindex)

    return pd.Series(y, index=timeindex)
