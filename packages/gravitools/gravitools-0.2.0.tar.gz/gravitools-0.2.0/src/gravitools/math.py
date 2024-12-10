from math import trunc

import allantools
import numpy as np
import pandas as pd


def calculate_allan_dev(ds, taus="octave", measurement_rate=None):
    """Calculate the overlapped Allan deviation of a time series.

    Args:
        ds (pd.Series):
            Time series of frequency input data.
        taus (np.array or str):
            Time differences (tau), in seconds, for which the Allan deviation is
            calculated. Specify "all", "octave" or "decade" for automatic
            generation. See `allantools.oadev` documentation.
        measurement_rate (float):
            Sampling rate of the input data, in Hz. Specify *None* to calculate
            from average interval.

    Returns:
        (pd.Series): Allan deviation at different taus
    """

    # Subtract global offset to avoid numeric precision limitations
    ds = ds - ds.iloc[0]

    if measurement_rate is None:
        seconds_total = (ds.index[-1] - ds.index[0]) / np.timedelta64(1, "s")
        measurement_rate = (len(ds) - 1) / seconds_total

    t, allan_dev, _, _ = allantools.oadev(
        ds.values, rate=measurement_rate, data_type="freq", taus=taus
    )

    adev = pd.Series(allan_dev, index=t, name="adev")
    adev.index.name = "tau"
    return adev


def interval_means(series, interval, min_count=None, name=None, err="sem"):
    """Calculate interval means of a time series

    See [pandas.DataFrame.resample](
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html).

    Args:
        series (pd.Series):
            Input time series.
        interval (str):
            Resampling interval, e. g. "1h".
        min_count (int | float):
            Minimum number of samples required in each interval. For intervals
            with fewer samples, the mean value is set to NaN. A fractional
            value `0 < min_count < 1` is interpreted as a fraction of the
            maximum number of samples.
        name (str):
            Prefix of the output dataframe's columns.  If unspecified, the
            input series' `name` attribute is used, or "y", if it does not have
            a name.
        err (str):
            Statistical function to use for error column. Options are "sem"
            (standard error of the mean) and "std" (standard deviation).

    Returns:
        (pd.DataFrame):
            Time series of mean value, standard error of the mean (SEM), and
            count of samples per interval.
    """

    # Shift interval such that index value is at the center (default is
    # beginning)
    offset = pd.tseries.frequencies.to_offset(interval) / 2

    name = name or series.name or "y"

    # Calculate interval means, SEM and sample count
    means = series.resample(interval, offset=offset).mean().to_frame(name)
    if err == "sem":
        means[name + "_err"] = series.resample(interval, offset=offset).sem()
    elif err == "std":
        means[name + "_err"] = series.resample(interval, offset=offset).std()
    else:
        raise ValueError(f"Parameter 'err' should be 'sem' or 'std', but is {err!r}.")
    means[name + "_count"] = series.resample(interval, offset=offset).count()
    means.index += offset

    # Remove interval means with low sample count
    if min_count:
        if min_count < 1.0:  # Specified as fraction of samples
            min_count *= means[name + "_count"].max()
        means.loc[means[name + "_count"] < min_count, name] = float("nan")

    return means


def truncate(x, digits=0):
    """Truncate a float number to specified digits"""
    return trunc(x * 10**digits) / 10**digits


def weighted_mean(values, errors):
    """Weighted mean, standard deviation and standard error of the mean"""
    # Remove values that are NaN in values or errors
    isnan = np.isnan(values) | np.isnan(errors)
    if isnan.any():
        values, errors = values[~isnan], errors[~isnan]

    if len(values) == 1:
        return values[0], errors[0], errors[0]

    # Weighting coefficients
    weights = 1 / (errors**2)
    weights /= weights.sum()

    # Weighted mean
    mean = np.average(values, weights=weights)

    # Weighted standard deviation
    std = np.sqrt(np.average((values - mean) ** 2, weights=weights))

    # Weighted standard error of the mean
    # See: https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
    sem = std * np.sqrt(np.sum(weights**2))

    return mean, std, sem
