from configparser import ConfigParser
import logging
import re

from ..quantity import (
    clean_coord_angle,
    clean_gradient,
    clean_height,
    clean_orientation,
    clean_pressure_admittance,
)
from ..utils import to_path

logger = logging.getLogger(__name__)


def parse_aqg_info_text(text: str) -> dict:
    """Parse text of an AQG .info file without cleaning up the content"""
    header_line, _, contents = text.partition("\n")
    if "AQG measurement report" not in header_line:
        raise ValueError("Incorrect AQG .info header: {header_line!r}")
    config = ConfigParser()
    config.read_string(contents)
    return {section: dict(config.items(section)) for section in config.sections()}


def get_aqg_meter(version: dict) -> str:
    hw = version.get("hardware")
    serial = version.get("id", "")
    if not serial:
        # Early versions of AQGui did not have the "id" key
        hw, serial = hw[0], hw[1:]
    return f"AQG-{hw}{serial.zfill(2)}"


def get_tide_components(tide):
    return [value for key, value in tide.items() if key.startswith("comp")]


def guess_point_and_orientation(site_name: str) -> dict:
    """Guess point code and setup orientation from the site name

    Examples:
        >>> guess_point_and_orientation("WET_FA_180")
        {'point': 'WET_FA', 'orientation': '180.0°'}

        >>> guess_point_and_orientation("WET_FA")
        {'point': 'WET_FA'}

        >>> guess_point_and_orientation("ALT_4334_AA_180")
        {'point': 'ALT_4334_AA', 'orientation': '180.0°'}

    Args:
        site_name:
            Identifier of the measurement location

    Returns:
        Dictionary of point and orientation values.
    """
    for pattern in [
        r"(?P<point>\w+)_(?P<orientation>\d{3})",
        r"(?P<point>\w+)",
    ]:
        if match := re.match(pattern, site_name):
            data = match.groupdict()
            if "orientation" in data:
                data["orientation"] = clean_orientation(data.get("orientation"))
            return data
    return {}


def clean_aqg_metadata(info: dict) -> dict:
    """
    Process the metadata from an AQG .info file

    Args:
        info: Unaltered parameters from an AQG .info file.

    Returns:
        Cleaned metadata
    """
    correction = info["correction"]
    location = info["location"]
    tide = info["tide_model"]
    version = info["version"]

    # Pick only what is needed
    metadata = {
        # Instrument
        "meter": get_aqg_meter(version),
        "software": version["software"],
        # Location
        "location_name": location["name"],
        "site_name": location.get("measurement_site_name", ""),
        "description": location.get("measurement_description", ""),
        "latitude": clean_coord_angle(location["latitude"]),
        "longitude": clean_coord_angle(location["longitude"]),
        "altitude": clean_height(location["altitude"]),
        # Correction
        "tripod_base_height": clean_height(correction["tripod_base_height"]),
        "instrument_factory_height": clean_height(
            correction["instrument_factory_height"]
        ),
        "reference_height": clean_height(correction["measurement_reference_height"]),
        "pressure_admittance": clean_pressure_admittance(
            correction["pressure_admittance"]
        ),
        "vgg": clean_gradient(correction["vgg"]),
        "tide_model_location": tide["location"],
        "tide_model_name": tide["model"],
        "tide_model_components": get_tide_components(tide),
        # Parameters missing in .info file
        "syst_uncertainty": None,
        "tilt_offset_x": None,
        "tilt_offset_y": None,
        "point": None,
        "orientation": None,
    }

    metadata.update(
        guess_point_and_orientation(
            metadata.get("site_name") or metadata.get("description")
        )
    )

    return metadata


def read_aqg_info(path):
    """Read an AQG .info file and parse the relevant metadata

    Args:
        path (str | pathlib.Path | zipfile.Path):
            Path to .info file.

    Returns:
        (dict): Metadata
    """
    logger.debug(f"Read {path}")
    text = to_path(path).read_text(encoding="utf-8")
    metadata = parse_aqg_info_text(text)
    return clean_aqg_metadata(metadata)
