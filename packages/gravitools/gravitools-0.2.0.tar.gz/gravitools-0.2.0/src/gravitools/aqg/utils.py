"""
Common constants and functions for AQG data analysis
"""

import pandas as pd

from ..utils import map_index, read_csv_files, sort_paths_numerically

AQG_SENSITIVITY = 500
"""Nominal AQG sensitivity, nm/s²*sqrt(Hz)"""


def rename_columns(names):
    """Rename column names to shorten and remove symbols

    Args:
        names (list[str]): Original column names.

    Returns:
        (dict): Mapping of original to new column names.
    """
    return {
        column: column.split(" (")[0]
        .lower()
        .replace(".", "_")
        .replace(" ", "_")
        .replace("__", "_")
        .replace("standard_deviation", "std")
        .replace("delta_g", "dg")
        .replace("raw_vertical_gravity", "g_raw")
        .replace("corrected_vertical_gravity", "g")
        .replace("ap_cooler_ap", "cooler")
        .replace("ap_cooler_rep_ap", "rep")
        for column in names
    }


def aqg_dtypes(names):
    """Change data types of columns to save memory space

    Args:
        names (list[str]):
            Column names.

    Returns:
        (dict):
            Mapping of column name to new data type.
    """
    dtypes = {
        col: "float32"
        for col in names
        if col.startswith("dg_")
        or "temperature" in col
        or "tilt" in col
        or "pressure" in col
        or col.endswith("_eta")
        or col.endswith("_phi")
        or col.endswith("_std")
    }
    dtypes["sat_abs_offset_correction"] = "int32"
    dtypes["sat_abs_offset_correction_applied"] = "bool"
    return dtypes


def clean_aqg_dataframe(df):
    """Clean dataframe of AQG rawdata from a CSV file

    Args:
        df (pd.DataFrame):
            Input dataframe, modified in place.
    """

    # Convert epoch seconds to pd.Timestamp
    for col in [
        "timestamp (s)",
        "estimated measure timestamp (s)",
    ]:
        if col in df:
            df.index = pd.to_datetime(df[col], utc=True, unit="s")
            df.index.name = "utc"
            break
    else:
        raise ValueError("No time column found")

    # Remove redundant columns
    drop_cols = [
        "timestamp (s)",
        "time (utc)",
        "date (utc)",
        "estimated measure timestamp (s)",
        "estimated measure date (utc)",
        "estimated measure time (utc)",
        # Remove original height transfer correction to avoid ambiguity
        "delta_g_height (nm/s^2)",
    ] + [col for col in df if "Unnamed:" in col]
    df.drop(columns=drop_cols, errors="ignore", inplace=True)

    # Rename columns
    df.rename(columns=rename_columns(list(df)), inplace=True)

    # Adjust data types to save memory
    df.astype(aqg_dtypes(list(df)))

    # Convert tilt angles from mrad to rad
    df.loc[:, ["x_tilt", "y_tilt"]] *= 1e-3

    return df.sort_index()


def read_aqg_csvs(paths):
    """Read multiple .csv files of AQG raw data.

    Args:
        paths (list[str | pathlib.Path | zipfile.Path]):
            Paths of .csv files to read.

    Returns:
        (pd.Dataframe):
            Data read from .csv files.
    """
    return clean_aqg_dataframe(read_csv_files(sort_paths_numerically(paths)))


def merge_aqg_raw_dataframes(df_raw, df_preprocessed):
    """Merge dataframes of AQG rawdata and preprocessed data

    The AQG rawdata folder contains CSV files of the full raw data and CSV
    files of preprocessed data in intervals with additional temperature
    columns. This function merges the dataframes into one for easier handling.

    Argument `df_raw` is modified in place.
    """

    # Integrate temperatures
    for col in ["external_temperature", "laser_temperature"]:
        df_raw[col] = map_index(df_preprocessed[col], df_raw.index)

    return df_raw
