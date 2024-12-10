"""
Common utility functions
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Mapping
import datetime
import logging
import multiprocessing
from pathlib import Path
import re
from typing import Callable
import zipfile

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

STANDARD_HEIGHT = 1.25  # m
"""Standard height above point marker for absolute gravity measurement."""


def interpolate_time_series(
    series: pd.Series, index: pd.DatetimeIndex, name: str = None
) -> pd.Series:
    """Linearly interpolate time series to new time index

    Time indices outside the bounds of the input data will return *NaN* values.

    Args:
        series: Input time series.
        index: New time index.
        name: Name of new time series. Taken from input series, if unspecified.

    Returns:
        Linear interpolation of input time series at specified time indices.
    """

    return pd.Series(
        np.interp(
            index, series.index, series.values, left=float("nan"), right=float("nan")
        ),
        index=index,
        name=name or series.name,
    )


def map_index(ser, index):
    """Map a time series to a different time index"""
    # same index values exist
    s1 = ser.reindex(index).dropna()
    # remaining rows
    s2 = ser[ser.index.difference(s1.index)]
    # find last earlier index
    s2 = s2.reindex(index, method="backfill", limit=1).dropna()
    # return combined series
    return pd.concat([s1, s2]).sort_index()


def flatten(d, lvl=0, prefix=None, sep="__"):
    """Flatten a nested dictionary"""
    out = OrderedDict()
    for k, v in sorted(d.items()):
        name = (prefix + sep if prefix else "") + str(k)
        if isinstance(v, dict):
            out.update(flatten(v, lvl + 1, name))
        else:
            # Convert Timstamp to str because it cannot be saved as xarray.Dataset
            # attribute
            out[name] = str(v) if isinstance(v, pd.Timestamp) else v
    return out


def iter_zipfile_path(zippath):
    """Recursively iterate all files within a zipfile.Path"""
    for path in zippath.iterdir():
        if path.is_dir():
            yield from iter_zipfile_path(path)
        else:
            yield path


def files_in_path(path):
    """List all files in a directory or zip-archive

    Args:
        path (str | pathlib.Path | zipfile.Path):
            Directory path.

    Returns:
        (list[pathlib.Path | zipfile.Path]): List of paths
    """
    path = to_path(path)

    if isinstance(path, zipfile.Path):
        # Path must be a folder within a zip-archive
        if not Path(path.root.filename).exists():
            raise FileNotFoundError(path.root.filename)
        if path.at:
            # Subfolders need to have '/' as suffix for exists() to work
            if path.at[-1] != "/":
                path.at = path.at + "/"
            if not path.exists():
                raise FileNotFoundError(path)
        return list(iter_zipfile_path(path))

    # Path must be a regular folder
    if not Path(path).exists():
        raise FileNotFoundError(path)
    if not path.is_dir():
        raise NotADirectoryError(path)
    return list(path.rglob("*"))


def filename_matches_pattern(path, pattern):
    r"""Compare filename against a regex pattern

    Examples:
        >>> filename_matches_pattern("path/to/test_123.csv", r"^test_\d+.csv$")
        True

    Args:
        path (str | pathlib.Path | zipfile.Path):
            Input path.
        pattern (str):
            Regex pattern.

    Returns:
        (bool): True, if match.
    """  # noqa: W605
    if isinstance(path, str):
        path = Path(path)
    return bool(re.search(pattern, path.name))


def read_csv(path):
    """Wrapper around pd.read_csv() to read files within zip-archives"""
    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, tuple):
        zipfile_path, path_in_zipfile = path
        path = zipfile.Path(zipfile_path, path_in_zipfile)
    logger.debug(f"Read {path}")
    if isinstance(path, zipfile.Path):
        # Python 3.10 added support for 'encoding' parameter to open().
        # TODO: This can be removed, when Python 3.9 support is dropped.
        with path.open() as f:
            return pd.read_csv(f)
    with path.open(encoding="utf-8") as f:
        return pd.read_csv(f)


def read_csv_files(paths):
    """Read CSV files in parallel"""
    # Pool.map() cannot pickle zipfile.Path, use tuple instead
    paths = [
        (p.root.filename, p.at) if isinstance(p, zipfile.Path) else p for p in paths
    ]
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        return pd.concat(p.map(read_csv, paths))


def to_path(input_path):
    """Convert to pathlib.Path or zipfile.Path

    Examples:
        >>> to_path("path/to/filename.txt")
        PosixPath('path/to/filename.txt')

        >>> to_path("path/to/archive.zip") # doctest: +SKIP
        zipfile.Path('path/to/archive.zip', '')

        >>> to_path("path/to/archive.zip/testfile.txt") # doctest: +SKIP
        zipfile.Path('path/to/archive.zip', 'testfile.txt')

    Args:
        input_path (str | pathlib.Path | zipfile.Path):
            Input path.

    Returns:
        (pathlib.Path | zipfile.Path): Output path.
    """
    if isinstance(input_path, zipfile.Path):
        return input_path
    path = Path(input_path)
    if ".zip" in str(input_path):
        for parent in [path] + list(path.parents):
            if parent.suffix == ".zip":
                rel = path.relative_to(parent)
                return zipfile.Path(parent, str(rel) if rel.name else "")
    return path


def sort_paths_numerically(paths):
    """Sort file paths by trailing number

    Examples:
        >>> sort_paths_numerically(["raw_10.csv", "raw_11.csv", "raw_9.csv"])
        ['raw_9.csv', 'raw_10.csv', 'raw_11.csv']
    """
    # AQG datasets can also have only one _raw.csv file that does not conform
    # to this numbering format.
    if len(paths) == 1:
        return paths
    return sorted(paths, key=lambda p: int(str(p)[:-4].rsplit("_", maxsplit=1)[-1]))


def get_const_columns(df, columns):
    """Check if columns are constant and return their value

    Args:
        df (pd.DataFrame): Input dataframe.
        columns (list[str]): List of column names to check.

    Returns:
        (dict): Names and values of constant columns.
    """
    return {
        column: df[column].iloc[0]
        for column in columns
        if all(df[column].values == df[column].iloc[0])
    }


def merge_dicts(d1: dict, d2: dict) -> dict:
    """Merge two nested dictionaries

    `d2` takes precedence over `d1`.

    Examples:
        >>> merge_dicts({"a": 1, "b": {"x": 1, "y": 0}}, {"b": {"y": 2, "z": 3}})
        {'a': 1, 'b': {'x': 1, 'y': 2, 'z': 3}}
    """
    return {
        key: (
            merge_dicts(d1[key], d2[key])
            if isinstance(d1.get(key), Mapping) and isinstance(d2.get(key), Mapping)
            else d2.get(key, d1.get(key))
        )
        for key in sorted(set(d1) | set(d2))
    }


def partition_dict(
    dictionary: dict, condition: Callable[[str], bool]
) -> tuple[dict, dict]:
    """Partition a dictionary by a condition on each key

    Args:
        dictionary: Input dictionary.
        condition: Callback function defining condition on key.

    Examples:
        >>> partition_dict({"a": 1, "b": 2}, lambda key: key.startswith("a"))
        ({'a': 1}, {'b': 2})

    """
    including = {key: value for key, value in dictionary.items() if condition(key)}
    excluding = {key: value for key, value in dictionary.items() if not condition(key)}
    return including, excluding


def is_date(text: str | datetime.date | datetime.datetime) -> bool:
    """Check if input is a date or a string that has date format

    Accepted formats are: `YYYY-mm-dd` and `YYYY-mm-dd HH:MM`.

    There is no check, whether this date is actually valid.
    """
    if isinstance(text, (datetime.date, datetime.datetime)):
        return True
    pattern = r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?$"
    return bool(re.search(pattern, text))
