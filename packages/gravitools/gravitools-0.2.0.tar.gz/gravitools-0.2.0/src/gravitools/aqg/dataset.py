"""
Handling of processed AQG data
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from ..quantity import AbsGValue, Gradient, parse_gravity, parse_height
from ..timeseries import GravityTimeSeries
from ..utils import STANDARD_HEIGHT, interpolate_time_series
from .utils import AQG_SENSITIVITY

logger = logging.getLogger(__name__)


default_report = None


class AQGDataset:
    """Processed AQG dataset

    Args:
        ds (XArray.Dataset): Dataset of processed AQG data
    """

    def __init__(self, ds):
        self.ds = ds

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def metadata(self):
        """Metadata attributes"""
        return self.ds.attrs

    @property
    def time_span(self) -> tuple:
        """Measurement start and end time"""
        return tuple(self.get("g").index[[0, -1]])

    @property
    def duration(self) -> pd.Timedelta:
        """Total duration of measurement"""
        t0, t1 = self.time_span
        return t1 - t0

    @property
    def num_drops(self) -> int:
        """Total number of drops"""
        return len(self.get("g"))

    @property
    def num_outliers(self) -> int:
        """Number of drops marked as outliers"""
        return int(self.get("is_outlier").sum())

    @property
    def h(self) -> float:
        """Measurement reference height, in meters"""
        return parse_height(self.metadata["reference_height"])

    @property
    def name(self) -> str:
        """Dataset identifier"""
        return self.metadata["name"]

    @property
    def comment(self) -> str:
        """Comment text"""
        return self.metadata.get("comment", "")

    @property
    def columns(self) -> list[str]:
        """List of data columns"""
        return list(self.ds)

    @property
    def temperature_columns(self) -> list[str]:
        """List of temperature data columns"""
        return [c for c in self.columns if c.endswith("_temperature")]

    @property
    def meter(self) -> str:
        """Instrument identifier"""
        return self.metadata["meter"]

    @property
    def point(self) -> str:
        """Measurement point identifier"""
        # enforce string because there will be a bug in PDF file creation if
        # point name is integer
        return str(self.metadata["point"])

    @property
    def orientation(self) -> int:
        return self.metadata["orientation"]

    @property
    def vgg(self) -> Gradient:
        """Vertical gravity gradient used for height transfer"""
        # TODO: Include gradient uncertainty
        return Gradient.from_str(self.metadata["vgg"])

    @property
    def syst_uncertainty(self) -> float:
        """Systematic uncertainty of the instrument"""
        return float(parse_gravity(self.metadata.get("syst_uncertainty") or 0))

    def get(self, column: str) -> pd.Series:
        """Retrieve a data column as Pandas series

        Args:
            column: Column name.

        Returns:
            Time series.
        """
        return self.ds[column].to_series()

    def full_g(self, h=STANDARD_HEIGHT, incl_outliers=False, **kwargs):
        """Full gravity signal

        Args:
            h (float):
                Transfer height. Pass None to use original height.
            incl_outliers (bool): Include drops marked as outliers.

        Returns:
            (GravityTimeSeries): Time series of gravity values
        """
        g = self.get("g")
        if not incl_outliers:
            # Exclude outliers
            g = g[~self.get("is_outlier")]
        full_g = GravityTimeSeries(
            g, height=self.h, vgg=self.vgg, label=self.name, **kwargs
        )
        if h is None:
            # No transfer height
            return full_g
        return full_g.transfer(h)

    def g(self, h=STANDARD_HEIGHT, incl_outliers=False, min_count=0.5, **kwargs):
        """Gravity signal resampled to 10 sec intervals

        Args:
            h (float):
                Height (in meters) to transfer gravity signal to using gravity gradient.
            incl_outliers (bool): Include drops marked as outliers.
            min_count (bool):
                Minimum number of drops required in an interval to be valid.

        Returns:
            (GravityTimeSeries): Time series of gravity values.
        """
        return self.full_g(h=h, incl_outliers=incl_outliers, **kwargs).resample(
            "10s", min_count=min_count
        )

    def mean(self, t0=None, t1=None, h=STANDARD_HEIGHT, incl_outliers=False):
        """Mean gravity value.

        Note:
            Estimating the AQG's statistical error is not trivial because the
            signal does not follow a normal distribution. Moreover, the noise
            characteristic can depend on location. This procedure is intended
            as a standard workflow that errs on the side of overestimating the
            uncertainty.

        The mean value is calculated from the unweighted mean of all accepted
        drops.

        For the calculation of the statistical error, the full signal is first
        downsampled to 10 second intervals (see method
        [g()][gravitools.aqg.dataset.AQGDataset.g]) because the AQG signal does
        not show a normal distribution below this time scale.

        For short measurements (< 2 hours), the statistical error is then
        calculated by the standard error of the mean (SEM) of the 10s-interval
        means.

        For longer (> 2 hours) measurements, the AQG signal typically does not
        show a normal distribution anymore (flicker noise), so the SEM would be
        an underestimation. Instead, the statistical error is estimated from
        the standard deviation of 1 hour interval means, i. e. the error will
        not decrease with measurement duration.

        If `t0` and `t1` are unspecified (`None`), the entire time series is
        used.

        Args:
            t0 (str, pd.Timestamp):
                Start of time range.
            t1 (str, pd.Timestamp):
                End of time range.
            h (float):
                Transfer height, in meters. Pass None for original height.
            incl_outliers (bool):
                Include drops marked as outliers.

        Returns:
            (AbsGValue): Mean absolute gravity value.
        """
        # Simple mean of all drops
        full_g = self.full_g(h=h, incl_outliers=incl_outliers)[t0:t1]
        g_mean = full_g.y.mean()
        h = full_g.height

        # Downsample to 10s intervals because the gravity signal does not have
        # a normal distribution below this time scale.
        g10s = self.g(h=h, incl_outliers=incl_outliers)[t0:t1]
        if self.duration < pd.Timedelta("2h"):
            # Unweighted standard error of the mean of 10 second intervals
            g_err = g10s.y.sem()
        else:
            # Weighted standard deviation of 1h means
            g_err = g10s.resample("1h").std()

        return AbsGValue(value=g_mean, error=g_err, height=h, vgg=self.vgg)

    def adev(self, t0=None, t1=None, incl_outliers=False):
        """Calculate the Allan deviation

        Note:
            The Allan deviation assumes a fixed-interval time series.  AQG data
            is nominally in 540 ms intervals, but can have gaps due to
            calibrations. This calculation assumes an interval of 540 ms, i. e.
            the gaps are pulled together.

        Args:
            t0 (str | pandas.Timestamp):
                Start of time range for calculation.
            t1 (str | pandas.Timestamp):
                End of time range for calculation.
            incl_outliers (bool):
                Include drops marked as outliers.

        Returns:
            (pandas.Series): Allan deviation.
        """
        mrate = 1 / 0.54  # Hz
        return self.full_g(incl_outliers=incl_outliers)[t0:t1].adev(mrate=mrate)

    def compare(self, g_ref, h=STANDARD_HEIGHT, incl_outliers=False):
        """Compare gravity time series to a reference function

        Args:
            g_ref (pd.Series): Gravity reference function.
            incl_outliers (bool):
                Include drops marked as outliers.

        Returns:
            (pandas.DataFrame):
                Dataframe of AQG signal, reference and difference.
        """
        df = self.g(h=h, incl_outliers=incl_outliers).y.to_frame(name="g_aqg")
        df["g_ref"] = interpolate_time_series(g_ref, df.index)
        df["dg"] = df["g_aqg"] - df["g_ref"]
        return df

    def to_nc(self, path):
        """Export dataset as NETCDF4 file

        Args:
            path (str | pathlib.Path): Path of .nc file to write to.
        """
        # Remove first because there can be errors if it already exists
        Path(path).unlink(missing_ok=True)

        # Use compression
        encoding = {v: dict(zlib=True, complevel=5) for v in self.ds}

        # Variable-length data types cannot be compressed. Change dtype of
        # string columns to zero-terminated fixed-length string. This issue was
        # introduced with netcdf4-python 1.6.0.
        for var in self.ds:
            if self.ds[var].dtype == object and isinstance(self.ds[var].values[0], str):
                max_len = self.ds[var].str.len().values.max()
                encoding[var]["dtype"] = f"S{max_len}"

        logger.info(f"Write {path}")
        self.ds.to_netcdf(path, format="NETCDF4", encoding=encoding)

    def plot_adev(
        self, t0=None, t1=None, incl_outliers=False, spec=True, ax=None, **kwargs
    ):
        """Plot of the Allan deviation

        Args:
            t0 (str | pandas.Timestamp):
                Start of time range to select for calculation.
            t1 (str | pandas.Timestamp):
                End of time range to select for calculation.
            incl_outliers (bool):
                Include drops marked as outliers.
            spec (bool):
                Plot sensitivity specification, to serve as visual reference.
            ax (matplotlib.axes.Axes):
                Plot axes.
            **kwargs (dict):
                Additional arguments to pass to `matplotlib.pyplot.plot`.

        Returns:
            (matplotlib.lines.Line2D):
                Plot line as returned by `matplotlib.pyplot.loglog`.
        """
        ax = ax or plt.gca()
        if "label" not in kwargs:
            kwargs["label"] = self.name
        plot = ax.loglog(self.adev(t0=t0, t1=t1, incl_outliers=incl_outliers), **kwargs)
        if spec:
            tau = np.array([10, 1e4])
            sensitivity = pd.Series(AQG_SENSITIVITY / np.sqrt(tau), index=tau)
            ax.loglog(sensitivity, "k--", linewidth=1)
        ax.set_xlabel(r"$\tau$ [s]")
        ax.set_ylabel(r"$\sigma(\tau)$ [nm/s²]")
        return plot

    def plot_full(
        self,
        t0=None,
        t1=None,
        height=None,
        incl_outliers=True,
        density=True,
        g0=None,
        ylim=(-2000, 2000),
        ax=None,
        **kwargs,
    ):
        """Plot full gravity time series

        Args:
            t0 (str |  pandas.Timestamp):
                Start of time range to select.
            t1 (str |  pandas.Timestamp):
                End of time range to select.
            height (float):
                Transfer height, in meters. Pass `None` for original
                measurement height.
            incl_outliers (bool):
                Include drops marked as outliers.
            density (bool):
                Visualize sample density.
            g0 (float):
                Offset on y-axis. Pass `None` for mean value.
            ylim (tuple):
                Y-axis plot range, in nm/s².
            ax (matplotlib.axes.Axes):
                Plot axes.
            **kwargs (dict):
                Additional arguments to pass to `matplotlib.pyplot.plot`.

        Returns:
            (matplotlib.lines.Line2D):
                Plot line as returned by `matplotlib.pyplot.plot`.
        """
        ax = ax or plt.gca()
        g = self.full_g(h=height, incl_outliers=True)[t0:t1]
        is_outlier = self.get("is_outlier")[t0:t1]
        if g0 is None:
            g0 = g.y[~is_outlier].mean()
        plot = ax.plot(g.y[~is_outlier] - g0, **kwargs)
        if density:
            ax.plot(g.y[~is_outlier] - g0, ",w", alpha=0.05, **kwargs)
        if incl_outliers:
            ax.plot(g.y[is_outlier] - g0, ",r", **kwargs)
        ax.set_ylabel(f"$g$ - {g0:,.0f} [nm/s²] (h={g.height:.2}m)")
        if ylim:
            ax.set_ylim(*ylim)
        return plot

    def save_report(self, path, reportclass=None, **kwargs):
        """Generate a PDF report of the processed dataset"""
        if reportclass is None:
            reportclass = default_report
        if not reportclass:
            raise ValueError(
                "No report class specified. Pass reportclass argument, or set "
                "default_report."
            )
        reportclass(self, **kwargs).save(path)


def read_aqg_dataset(path):
    """Read processed AQG dataset from an .nc-file

    Args:
        path (str, pathlib.Path):
            Path to .nc file.

    Returns:
        (AQGDataset):
    """
    return AQGDataset(xr.open_dataset(str(path)))


class AQGDataCollection(AQGDataset):
    """A sequence of processed AQG datasets one one location

    Attributes:
        datasets : list of AQGDataset
            List of processed datasets that make up the collection
    """

    def __init__(self, datasets):
        self.datasets = datasets

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def metadata(self):
        """Dataset metadata"""
        # Take metadata from first dataset
        return self.datasets[0].metadata

    @property
    def columns(self):
        """List of data columns"""
        return self.datasets[0].columns

    def get(self, column):
        """Get a combined data column"""
        return pd.concat([dataset.get(column) for dataset in self.datasets])

    def to_nc(self, path):
        # Overwrite the to_nc() method of AQGDataset
        raise NotImplementedError()
