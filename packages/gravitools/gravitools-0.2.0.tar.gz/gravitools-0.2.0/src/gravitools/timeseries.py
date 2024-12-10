"""
Utilities for time series
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .math import calculate_allan_dev, interval_means, truncate, weighted_mean
from .quantity import AbsGValue


class TimeSeries:
    """A wrapper of pandas.Series for time series

    Args:
        obj (pandas.Series, pandas.DataFrame):
            Input data object with a time index. When passing a
            pandas.DataFrame, it is expected to have a data column `y` and
            optional columns `y_err`.  When passing a 1-dim.  series, it is
            converted to a pandas.DataFrame with one column named `y`.
        **kwargs (dict):
            Optional keyword arguments to be used for plotting.
    """

    # Names of attributes that will be passed on to derived instances
    _metadata = []

    def __init__(self, obj, **kwargs):
        self.args = kwargs
        if len(obj.shape) == 1:
            # Input data is a series
            if ("label" not in self.args) and obj.name:
                self.args["label"] = obj.name
            self.df = obj.to_frame(name="y")
        else:
            # Input data is a data frame with at least two columns
            self.df = obj
            if "y" not in self.df:
                raise ValueError("DataFrame is missing a `y` column.")

    def __repr__(self):
        s = f"{self.__class__.__name__}: {self.args.get('label', '')}\n"
        if self.meta:
            s += f"{self.meta}\n"
        return s + repr(self.df)

    def __getitem__(self, items):
        return self.__class__(self.df[items], **self.meta, **self.args)

    @property
    def meta(self):
        """Dict of meta attibutes"""
        return {m: getattr(self, m) for m in self._metadata}

    @property
    def y(self):
        """Main value column"""
        return self.df.y

    @property
    def y_err(self):
        """Error value column"""
        return self.df.y_err

    @property
    def y0(self):
        """Plot y-axis offset"""
        return 0

    @property
    def has_error(self):
        """True, if column of error values exists"""
        return "y_err" in self.df

    def mean(self):
        """Mean, standard deviation and standard error of the mean

        Mean, standard deviation and SEM are weighted, if the time series has
        an error column. See [weighted_mean][gravitools.math.weighted_mean].

        Returns:
            mean (float): Mean value.
            std (float): Standard deviation.
            sem (float): Standard error of the mean.
        """
        if self.has_error:
            return weighted_mean(self.y.values, self.y_err.values)
        return self.y.mean(), self.y.std(), self.y.sem()

    def std(self):
        """Standard deviation"""
        _, std, _ = self.mean()
        return std

    def resample(self, interval, min_count=None, err="sem", **kwargs):
        """Resample time series to new interval duration

        See [interval_means()][gravitools.math.interval_means].

        Args:
            interval (str):
                Resampling interval, e.g. "1h".
            min_count (int | float):
                Minimum number of samples required in interval. Intervals with
                fewer samples are evaluated as NaN.
            err (str):
                Statistical function to use for error column. Options are "sem"
                (standard error of the mean) and "std" (standard deviation).
            kwargs (dict):
                Keyword arguments to be updated on resulting TimeSeries.
                Unspecified keywords are inherited.

        Returns:
            (TimeSeries): Time series of resampled data.
        """
        df = interval_means(self.df.y, interval=interval, min_count=min_count, err=err)
        args = {**self.args, **kwargs}
        return self.__class__(df, **self.meta, **args)

    def mask(self, *args, **kwargs):
        """Mask samples by a condition and return as new TimeSeries"""
        return self.__class__(self.df.mask(*args, **kwargs), **self.meta, **self.args)

    def adev(self, taus="auto", mrate=None):
        """Calculate the Allan deviation

        Args:
            taus (str | numpy.array):
                Time interval values `tau` to calculate the Allan deviation at.
            mrate (float | str):
                Measurement rate, in Hz.

        Returns:
            (pandas.Series): Allan deviation
        """
        if mrate is None and self.y.index.freq is None:
            raise ValueError(
                "Time series has to have fixed-frequency to calculate Allan "
                "deviation. Specify `mrate` to assume a constant measurement "
                "rate."
            )
        mrate = mrate or pd.Timedelta("1s") / self.y.index.freq
        if taus == "auto":
            # Calculate taus from measurement rate to series duration
            duration = (self.y.index[-1] - self.y.index[0]) / pd.Timedelta("1s")
            taus = np.logspace(np.log10(1 / mrate), np.log10(duration), 50)
        return calculate_allan_dev(self.y.dropna(), taus=taus, measurement_rate=mrate)

    def plot(
        self, fmt=None, ax=None, y0=None, errorbars=True, min_count=None, **kwargs
    ):
        """Plot

        Args:
            fmt (str):
                Plot style
            ax (matplotlib.Axes):
                Plot axes
            y0 (float):
                Y-axis offset to be applied to data. Acquired from `y0` property,
                if unspecified.
            errorbars (bool):
                Plot errorbars, if possible.
            min_count (int | float):
                Minimum number of samples in an interval, given by column
                `y_count`, for a point to be plotted. Fractional values are
                considered relative to maximum count. Ignored, if there is no
                column `y_count`.
            kwargs (dict):
                Arguments to be passed to Matplotlib.
        """
        ax = ax or plt.gca()
        if y0 is None:
            y0 = self.y0
        args = {**self.args, **kwargs}
        fmt2 = args.pop("fmt", None)
        fmt = fmt or fmt2

        df = self.df
        if "y_count" in self.df and min_count:
            if min_count < 1:
                min_count *= self.df.y_count.max()
            df = df.mask(df.y_count < min_count)

        if errorbars and self.has_error:
            return ax.errorbar(df.y.index, df.y - y0, df.y_err, fmt=fmt or ".", **args)
        return ax.plot(df.y - y0, fmt or "-", **args)

    def plot_mean(self, sem=False, std=False, y0=None, ax=None, **kwargs):
        """Plot mean, standard deviation and standard error of the mean (SEM)"""
        ax = ax or plt.gca()
        if y0 is None:
            y0 = self.y0
        mean, std, sem = self.mean()
        ax.axhline(mean - y0, **kwargs)
        if sem:
            ax.axhspan(mean - sem - y0, mean + sem - y0, alpha=0.2, **kwargs)
        if std:
            ax.axhline(mean - std - y0, linestyle="--", **kwargs)
            ax.axhline(mean + std - y0, linestyle="--", **kwargs)

    def chunks(self, freq="1D"):
        """Itervate over time series by intervals

        Args:
            freq (str):
                Duration of time intervals, e. g. "1D" for day intervals.

        Yields:
            (TimeSeries): Segment of this time series
        """
        for period in pd.period_range(self.y.index[0], self.y.index[-1], freq=freq):
            yield self[period.start_time : period.end_time.round("1ms")], period

    def plot_chunks(self, freq="1D", ylim=None, **kwargs):
        """Plot time series in chunks"""
        for chunk, period in self.chunks(freq):
            plt.figure()
            chunk.plot(**kwargs)
            plt.xlabel(str(period), loc="left")
            plt.xlim(period.start_time, period.end_time.round("1ms"))
            if ylim is not None:
                plt.ylim(*ylim)
            plt.show()

    def plot_adev(self, mrate=None, ax=None, **kwargs):
        """Plot the Allan deviation"""
        ax = ax or plt.gca()
        args = self.args | kwargs
        plot = ax.loglog(self.adev(mrate=mrate), **args)
        ax.set_xlabel(r"$\tau$ [s]")
        ax.set_ylabel(r"$\sigma(\tau)$ [nm/s²]")
        return plot


class GravityTimeSeries(TimeSeries):
    """A time series of gravity values

    Args:
        obj (pandas.Series | pandas.DataFrame):
            Input data, see :class:`TimeSeries`.
        height (float):
            Measurement height, in meters.
        vgg (float):
            Vertical gravity gradient, in nm/s² per meter.
    """

    _metadata = ["vgg", "height"]

    def __init__(self, obj, height=None, vgg=None, **kwargs):
        self.height = height
        self.vgg = vgg
        super().__init__(obj, **kwargs)

    @property
    def y0(self):
        return truncate(self.y.mean(), -3)

    def transfer(self, h):
        """Transfer to another height using VGG

        Args:
            h (float): New height, in meters.

        Returns:
            (GravityTimeSeries): Height transferred gravity data.
        """
        if self.height is None:
            raise ValueError("No height given")
        if self.vgg is None:
            raise ValueError("No gradient given")
        df = (self.y + (h - self.height) * float(self.vgg)).to_frame(name="y")
        if self.has_error:
            df["y_err"] = self.y_err
        return GravityTimeSeries(df, height=h, vgg=self.vgg, **self.args)

    def mean_std(self):
        """Mean gravity value with standard deviation as error

        Returns:
            (AbsGValue): Absolute gravity value.
        """
        mean, std, _ = self.mean()
        return AbsGValue(mean, std, height=self.height, vgg=self.vgg)

    def plot(self, fmt=None, ax=None, y0=None, **kwargs):
        """Plot gravity time series"""
        ax = ax or plt.gca()
        if y0 is None:
            y0 = self.y0
        lines = super().plot(fmt, ax, y0, **kwargs)
        ax.set_ylabel(f"g - {y0:,.0f} [nm/s²] (h={self.height}m)")
        return lines

    def to_csv(self, path, float_format="%.2f", **kwargs):
        """Save to a CSV file"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"h = {self.height} m\n")
            f.write(f"vgg = {self.vgg}\n")
            self.df.to_csv(f, float_format=float_format, **kwargs)
