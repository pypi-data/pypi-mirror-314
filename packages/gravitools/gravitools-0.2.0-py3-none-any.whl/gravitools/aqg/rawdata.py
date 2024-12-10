"""
Functions and classes to handle the AQG's raw data files
"""

from __future__ import annotations

import logging
import pathlib
import zipfile

from packaging import version
import pandas as pd
import xarray as xr

from .. import __version__
from ..config import combine_dataset_config
from ..corrections import dg_polar, pressure_correction, tilt_correction
from ..outliers import (
    guess_mean_and_std,
    join_close_segments,
    reject_by_sigma_threshold,
    reject_by_threshold,
    reject_neighbors,
)
from ..quantity import (
    Gradient,
    GValue,
    clean_gradient,
    clean_gravity,
    clean_orientation,
    clean_pressure_admittance,
    clean_tilt_angle,
    format_height,
    parse_coord_angle,
    parse_height,
    parse_orientation,
    parse_pressure_admittance,
    parse_tilt_angle,
)
from ..utils import flatten, get_const_columns, interpolate_time_series, partition_dict
from .dataset import AQGDataset
from .files import find_aqg_raw_dataset_files
from .info import read_aqg_info
from .utils import merge_aqg_raw_dataframes, read_aqg_csvs

logger = logging.getLogger(__name__)


# Decorator marking methods that require corrections to be applied first
def apply_corrections_first(func):
    def wrapper_func(self, *args, **kwargs):
        if self._modified:
            self.apply_corrections()
        return func(self, *args, **kwargs)

    return wrapper_func


# Decorator marking methods that modify the raw data
def modifies(func):
    def wrapper_func(self, *args, **kwargs):
        self._modified = True
        return func(self, *args, **kwargs)

    return wrapper_func


class AQGRawData:
    """
    Dataframe of AQG rawdata

    This is a wrapper class for a pandas.DataFrame and a dictionary of
    metadata.

    Attributes:
        df (pandas.DataFrame):
            Full raw data
        metadata (dict):
            All metadata. Created from the .info file.
        name (str):
            Dataset identifier.
        _modified (bool):
            True, when columns where modified and the corrected signal has to be
            recalculated.
        log_entries (list[str]):
            List of log messages explaining processing steps taken.
    """

    @classmethod
    def from_files(cls, info_path, raw_csv_paths, csv_paths, name, source=None):
        """Read an AQGRawData instance from rawdata files

        Args:
            info_path (str | pathlib.Path | zipfile.Path):
                Path to AQG .info file.
            raw_csv_paths (list[str | pathlib.Path | zipfile.Path]):
                Paths to AQG _raw.csv files with one row per drop.
            csv_paths (list[str | pathlib.Path | zipfile.Path]):
                Paths to AQG .csv files of preprocessed data.
            name (str):
                Dataset identifier.
            source (str | Path):
                Data source identifier. If unspecified, `info_path` is taken.

        Returns:
            (AQGRawData): Raw data object.
        """
        # Read data files
        metadata = read_aqg_info(info_path)
        metadata["source"] = str(source) if source else str(info_path)
        df = merge_aqg_raw_dataframes(
            read_aqg_csvs(raw_csv_paths), read_aqg_csvs(csv_paths)
        )

        # Drop const. correction columns
        const_corrections = get_const_columns(
            df, ["dg_syst", "dg_ocean_loading", "dg_laser_polarization", "dg_quartz"]
        )
        if const_corrections:
            df.drop(columns=const_corrections, inplace=True)

        # Convert gravity correction values to quantity strings with units and
        # add them to the existing metadata
        const_corrections = {
            name: str(GValue(value))
            for name, value in const_corrections.items()
            if value  # Only keep non-zero corrections
        }
        metadata.update(const_corrections)

        return cls(df=df, metadata=metadata, name=name)

    def __init__(self, df, metadata, name):
        self.df = df
        self.metadata = metadata
        self.name = name
        self._modified = True
        self.log_entries = []
        if "is_outlier" not in self.df:
            self.df["is_outlier"] = False

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def variable_corrections(self):
        """List of correction columns in the dataframe"""
        return [column_name for column_name in self.df if column_name.startswith("dg_")]

    @property
    def const_corrections(self) -> dict[str, float]:
        """Constant gravity corrections in the metadata"""
        return {
            key: float(GValue.from_str(value))
            for key, value in self.metadata.items()
            if key.startswith("dg_")
        }

    @property
    def coordinate(self) -> tuple[float, float]:
        """Location latitude and longitude, in degree"""
        return (
            parse_coord_angle(self.metadata["latitude"]),
            parse_coord_angle(self.metadata["longitude"]),
        )

    @property
    def altitude(self) -> float:
        """Location altitude, in meters"""
        return parse_height(self.metadata["altitude"])

    @property
    def meter(self):
        """Instrument identifier"""
        return self.metadata["meter"]

    @property
    def point(self):
        """Measurement point identifier"""
        return self.metadata["point"]

    @property
    def orientation(self):
        """Measurement setup orientation"""
        orientation = self.metadata["orientation"]
        return parse_orientation(orientation) if orientation else None

    @property
    def vgg(self) -> Gradient:
        """Vertical gravity gradient"""
        return Gradient.from_str(self.metadata["vgg"])

    @property
    def pressure_admittance(self) -> float:
        """Atmospheric pressure admittance factor"""
        return parse_pressure_admittance(self.metadata["pressure_admittance"])

    @property
    def start_time(self) -> pd.Timestamp:
        """Time when the first data was recorded"""
        return self.df.index[0].round("1s")

    @property
    def tilt_offset(self) -> tuple(float, float):
        """Instrument tiltmeter offset angles"""
        x = self.metadata.get("tilt_offset_x")
        y = self.metadata.get("tilt_offset_y")
        return parse_tilt_angle(x) if x else None, parse_tilt_angle(y) if y else None

    def log(self, text):
        """Add a message to the processing log"""
        logger.debug(text)
        self.log_entries.append(text)

    def replace_metadata(
        self,
        *,
        default_orientation=None,
        orientation=None,
        pressure_admittance=None,
        syst_uncertainty=None,
        vgg=None,
        tilt_offset=None,
        **kwargs,
    ):
        """Replace metadata parameters

        Args:
            orientation (int):
                Sensor head setup orientation, in degree.
            default_orientation (int):
                Default sensor head setup orientation, if it is not yet
                explicitly specified.
            pressure_admittance (float):
                Atmospheric pressure admittance factor, in nm/s²/hPa.
            vgg (float | str):
                Gravity gradient, in nm/s²/m.
            tilt_offset (tuple, str):
                Instrument tiltmeter offset angles this dataset was recorded
                with. String is split by commas.
            **kwargs (dict):
                Additional metadata parameters. Parameters starting with
                prefix `dg_`, such as `dg_syst`, are interpreted as constant
                gravity corrections.
        """
        # orientation can have zero value, so check against None
        if orientation is not None:
            # Set explicit orientation. This might overwrite an orientation
            # value that was guessed from the site_name.
            self.metadata["orientation"] = clean_orientation(orientation)
        elif (
            default_orientation is not None and self.metadata.get("orientation") is None
        ):
            # Orientation is unknown, but a default is specified
            logger.debug(f"Assuming default setup orientation: {default_orientation}")
            self.metadata["orientation"] = clean_orientation(default_orientation)

        if pressure_admittance:
            self.set_pressure_admittance(pressure_admittance)
        if vgg:
            self.metadata["vgg"] = clean_gradient(vgg)
        if syst_uncertainty:
            self.metadata["syst_uncertainty"] = clean_gravity(syst_uncertainty)
        if tilt_offset:
            if isinstance(tilt_offset, str):
                tilt_offset = tilt_offset.split(",")
            if isinstance(tilt_offset, (tuple, list)):
                x, y = tilt_offset
            x = clean_tilt_angle(x)
            y = clean_tilt_angle(y)
            self.metadata["tilt_offset_x"] = x
            self.metadata["tilt_offset_y"] = y

        const_corrections, other = partition_dict(
            kwargs, lambda key: key.startswith("dg_")
        )
        for const_correction_name, value in const_corrections.items():
            self.set_const_correction(const_correction_name, value)
        self.metadata.update(other)

    def process(
        self,
        *,
        change_tilt_offset=None,
        recalculate_dg_pressure=True,
        recalculate_dg_polar=True,
        detect_outliers=None,
        outlier_ranges=None,
        station_height_difference=None,
        time_period=None,
        **metadata,
    ):
        """Apply a standard processing procedure to the dataset

        Args:
            change_tilt_offset (tuple[float, float]):
                Recalculate tilt angles and tilt correction for new tiltmeter
                offset.
            recalculate_dg_pressure (bool):
                Whether to call `recalculate_dg_pressure()`.
            recalculate_dg_polar (bool):
                Whether to call `recalculate_dg_polar()`.
            detect_outliers (dict | False):
                Parameters for outlier detection.  Pass a dictionary of
                parameters to override defaults of `detect_outliers()`.  Pass
                `None` to use default parameters.  Set `False` to deactivate.
            outlier_ranges (list):
                List of time ranges to mark as outliers. See
                `mark_outlier_ranges()`.
            station_height_difference (float):
                Offset to apply to the measurement reference height.
            time_period (tuple[str | pd.datetime, str | pd.datetime]):
                Tuple of start and end timestamps according to which the time
                series will be cut.
            **metadata (dict):
                Parameters to pass on to `replace_metadata()`.

        Returns:
            (AQGRawData): Itself.
        """
        if version.parse(self.metadata["software"]) < version.parse("1.4.5"):
            # Fix quartz correction for early AQGui version (2020-03-04)
            self.log("Double dg_quartz")
            self.df.loc[:, "dg_quartz"] *= 2

        self.replace_metadata(**metadata)

        if change_tilt_offset:
            # Recalculate tilt angles and then dg_tilt
            self.recalculate_tilt(change_tilt_offset)
        else:
            self.calculate_dg_tilt()
        if time_period is not None:
            self.limit_time_period(time_period[0], time_period[1])
        if recalculate_dg_pressure:
            self.calculate_dg_pressure()
        if recalculate_dg_polar:
            self.calculate_dg_polar()
        if detect_outliers is not False:
            if not isinstance(detect_outliers, dict):
                detect_outliers = {}
            self.detect_outliers(**detect_outliers)
        if outlier_ranges:
            self.mark_outlier_ranges(outlier_ranges)
        if station_height_difference is not None:
            self.shift_reference_height(station_height_difference)
        # Return self to allow direct call of to_dataset()
        return self

    def mark_outlier_ranges(self, time_ranges):
        """Mark a list of time ranges as outliers

        Args:
            time_ranges (list[tuple | str]):
                List of time ranges. Elements can be a tuple of two timestamps, or
                a string of format `START .. END`, where `START` and `END` are
                inputs to `pd.to_datetime()`.
        """
        for time_range in time_ranges:
            if isinstance(time_range, str):
                t0, t1 = pd.to_datetime(time_range.split(" .. "), utc=True)
            else:
                t0, t1 = time_range
            self.df.loc[t0:t1, "is_outlier"] = True

    @modifies
    def limit_time_period(self, t_from=None, t_to=None):
        """Limit the data time period to a certain interval

        Args:
            t_from (pd.datetime | str):
                Start time ...
            t_to (pd.datetime | str):
                ... and end time to which the data should be adjusted to.
                If provided as a string, this has to be in a format that is
                automatically parsable by standard conversion functions.
        """
        # if not provided, guess desired start_end dates:
        if t_from is None:
            t_from = self.df.index.min()
        if t_to is None:
            t_to = self.df.index.max()
        # make sure, this is really a date format
        # if not, convert it to that and reference as UTC
        t_from = pd.to_datetime(t_from, utc=True)
        t_to = pd.to_datetime(t_to, utc=True)
        # write log entry
        self.log(
            f"Modified time period of data from {t_from.strftime('%Y-%m-%d %H:%M:%S')} "
            f"to {t_to.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        # adjust time period
        self.df = self.df[t_from:t_to]

    @modifies
    def recalculate_tilt(self, tilt_offset):
        """Recalculate the tilt angles for a new tilt offset

        Args:
            tilt_offset (tuple[float, float]):
                New tilt offset angles, in radian.

        In order to reclculate tilt angles with a new tilt offset, the original
        tilt offset has to be known. This is currently not part of the AQG
        .info files, but can be found in the global AQG configruation file
        *settings.ini*.

        Set the original tilt offset manually by specifying it in the metadata:

            AQGRawData.metadata["tilt_offset"] = 1.234e-3, 0.123e-3  # radians
        """
        old_x, old_y = self.tilt_offset
        if old_x is None or old_y is None:
            raise ValueError(
                "Original tilt offset is unknown. Set metadata['tilt_offset_x'] and "
                "metadata['tilt_offset_y']."
            )
        fmt = "{tilt_offset_x}, {tilt_offset_y}"
        old_offset = fmt.format(**self.metadata)

        # Update metadata
        self.replace_metadata(tilt_offset=tilt_offset)
        new_x, new_y = self.tilt_offset
        new_offset = fmt.format(**self.metadata)

        # Update tilt angles
        self.log(f"Recalculate tilt with new offset: {old_offset} -> {new_offset}")
        self.df.loc[:, "x_tilt"] += old_x - new_x
        self.df.loc[:, "y_tilt"] += old_y - new_y

        # Update tilt correction
        self.calculate_dg_tilt()

    @modifies
    def set_dg_earth_tide(self, dg_earth_tide, name):
        """Replace the earth tide gravity correction time series

        The time series will be linearly interpolated to determine a correction
        for each drop.

        Args:
            dg_earth_tide (pandas.Series):
                Time series of gravity corrections.
            name (str):
                Tide model identifier name.
        """
        self.log(f"Replaced dg_earth_tide with {name}")
        self.df["dg_earth_tide"] = interpolate_time_series(dg_earth_tide, self.df.index)
        self.metadata["tide_model"] = dict(
            model=name, comment="Replaced in post-processing."
        )

    @modifies
    def set_pressure_admittance(self, admittance: float | str) -> None:
        """Change the admittance factor used for atmospheric pressure correction

        Args:
            admittance:
                New admittance factor. Pass a float value in units of
                nm/s²/hPa. Or pass a string value with adequate units, that can
                be parsed by
                [`parse_pressure_admittance()`][gravitools.quantity.parse_pressure_admittance].
        """
        # Normalize to string with conventional units
        text = clean_pressure_admittance(admittance)
        self.log(f"Change pressure admittance to {text}")
        # Keep string with units in metadata
        self.metadata["pressure_admittance"] = text

    def shift_reference_height(self, height_offset: float | str) -> None:
        """Apply an offset to the measurement reference height"""
        if isinstance(height_offset, str):
            height_offset = parse_height(height_offset)
        self.log(f"Shift reference height by {height_offset:+.4f} m")
        ref_height = parse_height(self.metadata["reference_height"])
        new_ref_height = ref_height + height_offset
        self.metadata["reference_height"] = format_height(new_ref_height)

    @property
    def dg_syst(self) -> float:
        """Const. systematic bias correction"""
        return float(GValue.from_str(self.metadata["dg_syst"]))

    @modifies
    def calculate_dg_pressure(self):
        """Recalculate the gravity correction due to atmospheric pressure"""
        self.log("Recalculate dg_pressure")
        self.df["dg_pressure"] = pressure_correction(
            self.df.atmospheric_pressure,
            altitude=self.altitude,
            admittance=self.pressure_admittance,
        )

    @modifies
    def calculate_dg_polar(self):
        """Recalculate the gravity correction due to polar motion"""
        self.log("Recalculate dg_polar")
        self.df["dg_polar"] = dg_polar(self.df.index, *self.coordinate)

    @modifies
    def calculate_dg_tilt(self):
        """Recalculate the instrument tilt gravity correction"""
        self.log("Recalculate dg_tilt")
        # There can be precision errors, if the tilt angle is float32
        self.df["dg_tilt"] = tilt_correction(
            self.df.loc[:, "g_raw"].astype("float64"),
            self.df.loc[:, "x_tilt"].astype("float64"),
            self.df.loc[:, "y_tilt"].astype("float64"),
        )

    def mark_outlier_range(self, t_start, t_end):
        """Mark a segment of drops as outliers"""
        t_start = pd.Timestamp(t_start, tz="utc")
        t_end = pd.Timestamp(t_end, tz="utc")
        self.log(f"Mark {t_start} to {t_end} as outliers")
        self.df.loc[t_start:t_end, "is_outlier"] = True

    @modifies
    def set_const_correction(self, name: str, value: float | str) -> None:
        """Set a constant bias correction"""
        if not name.startswith("dg_"):
            name = f"dg_{name}"
        # Convert to standard format string
        if isinstance(value, str):
            value = clean_gravity(value)
        else:
            # value is a number
            value = str(GValue(value))
        self.log(f"Set const. correction: {name} = {value}")
        self.metadata[name] = value

    def apply_corrections(self):
        """Calculate corrected gravity signal by applying all corrections"""
        var_corrections = self.variable_corrections
        const_corrections = self.const_corrections
        all_corrections = var_corrections + list(const_corrections)
        self.log("Apply corrections: " + ", ".join(all_corrections))

        # Calculate total of variable correction signal
        dg_var = self.df.loc[:, var_corrections].sum(axis=1).astype("float64")

        # Calculate total of constant corrections
        dg_const = sum(const_corrections.values())

        # Check that tilt correction does not have a sign error
        if "dg_tilt" in var_corrections and self.df.loc[:, "dg_tilt"].max() > 0:
            raise ValueError(
                "Tilt correction is positive. It should always be negative."
            )

        # Corrections are subtracted
        self.df.loc[:, "g"] = self.df.loc[:, "g_raw"] - dg_var - dg_const
        self._modified = False

    @apply_corrections_first
    def detect_outliers(
        self,
        g_true=None,
        g_std=None,
        threshold=2000,
        sigma_threshold=5,
        neighbors=20,
        min_gap="60s",
    ):
        """Identify and mark outliers in the gravity signal

        Drops that deviate from the mean `g_true` by more than `g_std` *
        `sigma_threshold` are considered outliers.

        Args:
            g_true (float):
                Gravity value to take as reference for calculation of outlier
                deviation. Pass `None` to have this value calculated
                automatically.
            g_std (float):
                Gravity signal standard deviation to use for sigma-criterion.
                Pass `None` for automatic calculation.
            threshold (float):
                Absolute threshold for maximum deviation.
            sigma_threshold (float):
                Multiplicator for standard deviation `g_std` defining outlier
                threshold.
            neighbors (int):
                Number of drops neighboring an outlier to also mark as
                outliers.
            min_gap (str):
                Minimum time gap between two outliers to be considered as
                separate events. Specify as `pandas.Timedelta` argument, e. g.
                '60s'.
        """
        # Write detection parameters to log. Skip inactive mechanisms.
        param = {
            "g_true": g_true,
            "g_std": g_std,
            "threshold": threshold,
            "sigma_threshold": sigma_threshold,
            "neighbors": neighbors,
            "min_gap": min_gap,
        }
        parameters = ", ".join(
            f"{key}={value}" for key, value in param.items() if value
        )
        self.log(f"Remove outliers: {parameters}")

        g = self.df.loc[:, "g"]
        is_outlier = pd.Series(False, index=g.index)
        if threshold:
            is_outlier |= reject_by_threshold(
                g, threshold=threshold, g_true=g_true or g.iloc[100:200].median()
            )
        if sigma_threshold:
            # Guess mean and standard deviation for sigma-criterion from
            # samples that are not yet marked as outliers.
            if not g_true or not g_std:
                g_true_guess, g_std_guess = guess_mean_and_std(g[~is_outlier])
                # Replace arguments, if unspecified
                g_true = g_true or g_true_guess
                g_std = g_std or g_std_guess
            is_outlier |= reject_by_sigma_threshold(
                g, sigma_threshold=sigma_threshold, g_true=g_true, g_std=g_std
            )
        if neighbors:
            is_outlier |= reject_neighbors(is_outlier, neighbors)
        if min_gap:
            is_outlier |= join_close_segments(is_outlier, min_gap)
        self.df["is_outlier"] = is_outlier

    @apply_corrections_first
    def to_dataset(self):
        """Create a finalized dataset of processing results

        Converts the `pandas.DataFrame` to an `xarray.Dataset` with metadata.

        Returns:
            (AQGDataset): Dataset of processed results
        """

        # Create xarray.Dataset from pandas.Dataframe
        # Remove time zome, because NETCDF4 does not handle it
        ds = xr.Dataset(self.df.tz_localize(None))

        # Transfer metadata
        metadata = {
            # NETCDF4 does not handle None values
            key: value if value is not None else ""
            for key, value in flatten(self.metadata).items()
        }
        metadata["name"] = self.name
        metadata["time_processed"] = f"{pd.Timestamp.utcnow().round('s')}"
        metadata["log"] = self.log_entries
        metadata["processing_software"] = f"gravitools {__version__}"
        for key, value in sorted(metadata.items()):
            ds.attrs[key] = value

        return AQGDataset(ds)


def read_aqg_raw_dataset(
    path: str | pathlib.Path | zipfile.Path, name: str = None
) -> AQGRawData:
    """Read an AQG raw dataset from a directory or zip-archive

    Args:
        path:
            Path to directory or zip-archive containing AQG raw data.
        name:
            Dataset identifier. If unspecified, the name is infered from the
            parent directory of the data files.

    Returns:
        Unprocessed AQG dataset
    """
    fileset = find_aqg_raw_dataset_files(path)
    # If no identifier is specified, take parent directory name as identifier
    name = name or str(fileset["info_path"].parent.name)
    logger.info(f"Read {path}")
    return AQGRawData.from_files(**fileset, name=name, source=path)


def process_aqg_raw_dataset(
    path: str | pathlib.Path | zipfile.Path,
    *,
    name: str = None,
    config: dict = None,
) -> AQGDataset:
    """Read and process an AQG raw dataset from a directory or zip-archive

    Applies standard processing procesdure. See
    [process()][gravitools.aqg.rawdata.AQGRawData.process].

    Args:
        path:
            Path to directory or zip-archive containing AQG raw data.
        name:
            Dataset identifier. If unspecified, the name is infered from the
            parent directory of the data files.
        config:
            Processing configuration parameters. The relevant parameters are
            selected using
            [combine_dataset_config][gravitools.config.combine_dataset_config].

    Returns:
        Processed AQG dataset
    """
    if config is None:
        config = {}
    raw = read_aqg_raw_dataset(path, name=name)
    cfg = combine_dataset_config(
        config, dataset=raw.name, meter=raw.meter, point=raw.point
    )
    logger.debug(f"Processing parameters: {cfg}")
    raw.process(**cfg)
    return raw.to_dataset()
