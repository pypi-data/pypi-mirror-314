"""Functions for outlier detection"""

import pandas as pd


def reject_by_threshold(g, threshold, g_true=None):
    """Reject samples that deviate by more than a threshold value

    Args:
        g (pd.Series):
            Input gravity time series.
        threshold (float):
            Maximum allowed deviation from reference value.
        g_true (float):
            Reference value to calculate deviation from. If unspecified, it is
            estimated from the median of the first 1000 samples.

    Returns:
        is_outlier (pd.Series):
            Time series of samples marked as outliers.
    """
    if g_true is None:
        g_true = g.head(1000).median()
    return (g - g_true).abs() > threshold


def guess_mean_and_std(g, interval="1min"):
    """Guess mean and standard deviation of signal with outliers

    Args:
        g (pd.Series):
            Input graviy time series.

    Returns:
        g_mean (float):
            Estimated mean.
        g_std (float):
            Standard deviation.
    """
    interval_means = g.resample(interval).mean()
    interval_std_devs = g.resample(interval).std()
    # Guess normal standard deviation from median standard deviation of
    # intervals
    median_std = interval_std_devs.median()
    # Guess true mean from quiet intervals (standard deviation lower than
    # median)
    mean = interval_means[interval_std_devs < median_std].mean()
    return mean, median_std


def reject_by_sigma_threshold(g, sigma_threshold, g_true=None, g_std=None):
    """Reject samples by a sigma criterion

    Args:
        g (pd.Series):
            Input graviy time series.
        sigma_threshold (float):
            Maximum allowed standard deviations.
        g_true (float):
            Reference value.
        g_std (float):
            Reference standard deviation.

    Returns:
        is_outlier (pd.Series):
            Time series of samples marked as outliers.
    """
    if g_std is None or g_true is None:
        mean, median_std = guess_mean_and_std(g)
        g_std = g_std or median_std
        g_true = g_true or mean
    return reject_by_threshold(g, threshold=sigma_threshold * g_std, g_true=g_true)


def reject_neighbors(is_outlier, num):
    """Reject nearest neighbors of outliers

    Args:
        is_outlier (pd.Series):
            Series of samples marked as outlier.
        num (int):
            Number of neighbors on either side to reject.

    Returns:
        is_outlier (pd.Series):
            Time series of samples marked as outlier with additionl neighbors
            marked.
    """
    win_size = 2 * num + 1
    return is_outlier.rolling(win_size, min_periods=0, center=True).mean() > 0


def get_outlier_segments(is_outlier, round_to="1s"):
    """List time segments of outliers

    Args:
        is_outlier (pd.Series):
            Time series of samples marked as outlier.

    Returns:
        (list[tuple[pd.Timestamp, pd.Timestamp]]):
            List of time ranges of outliers.
    """
    is_outlier = is_outlier.astype("int8")
    # Find first and last outlier samples
    edges = is_outlier.diff()
    # Mark first and last sample as start/end, if they are outliers
    edges.iloc[0] = is_outlier.iloc[0]
    edges.iloc[-1] = -is_outlier.iloc[-1]
    start_times = edges[edges > 0].index
    end_times = edges[edges < 0].index
    return [
        (t_start.floor(round_to), t_end.ceil(round_to))
        for t_start, t_end in zip(start_times, end_times)
    ]


def join_close_segments(is_outlier, min_gap):
    """Join outlier segments that are close together

    Args:
        is_outlier (pd.Series):
            Time series of samples marked as outlier.
        min_gap (str):
            Minimum time gap between outliers to allow. Outliers that are
            closer together are joined into one outlier segment.

    Returns:
        is_outlier (pd.Series):
            Time series of samples marked as outlier.
    """
    min_gap = pd.to_timedelta(min_gap)
    outlier_ranges = list(get_outlier_segments(is_outlier))
    mask = pd.Series(False, index=is_outlier.index)
    for (_, first_range_end), (next_range_start, __) in zip(
        outlier_ranges[:-1], outlier_ranges[1:]
    ):
        if next_range_start - first_range_end < min_gap:
            # Mark samples between ranges as outliers
            mask[first_range_end:next_range_start] = True
    return mask
