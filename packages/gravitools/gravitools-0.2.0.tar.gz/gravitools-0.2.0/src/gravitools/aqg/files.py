"""
Functions for handling sets of AQG raw data files
"""

import logging

from ..utils import filename_matches_pattern, files_in_path

logger = logging.getLogger(__name__)

AQG_INFO_FILENAME_PATTERN = r"^capture_\d{8}_\d{4,6}.info$"
AQG_RAW_CSV_FILENAME_PATTERN = r"^capture_\d{8}_\d{4,6}_raw(_\d+)*.csv$"
AQG_CSV_FILENAME_PATTERN = r"^capture_\d{8}_\d{4,6}(_\d+)*.csv$"


def is_aqg_info(path):
    """Filter for AQG .info files

    Examples:
        >>> is_aqg_info("path/capture_20240102_123456.info")
        True
    """
    return filename_matches_pattern(path, AQG_INFO_FILENAME_PATTERN)


def is_aqg_raw(path):
    """Filter for AQG .csv raw data files

    Examples:
        >>> is_aqg_raw("path/capture_20240102_123456_raw_1.csv")
        True
    """
    return filename_matches_pattern(path, AQG_RAW_CSV_FILENAME_PATTERN)


def is_aqg_csv(path):
    """Filter for AQG .csv preprocessed data files

    Examples:
        >>> is_aqg_csv("path/capture_20240102_123456_1.csv")
        True
    """
    return filename_matches_pattern(path, AQG_CSV_FILENAME_PATTERN)


def find_aqg_raw_dataset_files(path):
    """Find the set of AQG data files within a directory or archive

    Args:
        path (str | pathlib.Path | zipfile.Path):
            Path to directory or zip-archive.

    Returns:
        (dict): Dictionary of file paths.
    """
    # Find .info file
    info_files = list(filter(is_aqg_info, files_in_path(path)))
    if len(info_files) == 0:
        raise FileNotFoundError(f"No AQG .info file in {path}")
    if len(info_files) > 1:
        raise ValueError(f"Multiple AQG .info files in {path}")
    info_path = info_files[0]

    # Common stem of all data files (usually "capture_YYYYMMDD_HHMMSS")
    stem = info_path.name.split(".info")[0]

    # Find matching .csv files
    data_paths = [
        path
        for path in info_path.parent.iterdir()
        if path.name.startswith(stem) and path.name.endswith(".csv")
    ]
    raw_csv_paths = list(filter(is_aqg_raw, data_paths))
    csv_paths = list(filter(is_aqg_csv, data_paths))
    if len(raw_csv_paths) == 0:
        raise FileNotFoundError(f"No raw .csv files found for {info_path}")
    if len(csv_paths) == 0:
        raise FileNotFoundError(f"No preprocessed .csv files found for {info_path}")

    return {
        "info_path": info_path,
        "raw_csv_paths": raw_csv_paths,
        "csv_paths": csv_paths,
    }
