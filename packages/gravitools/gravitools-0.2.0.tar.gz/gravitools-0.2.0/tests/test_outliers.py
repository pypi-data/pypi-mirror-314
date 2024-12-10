import numpy as np
import pandas as pd
import pytest

from gravitools import outliers


def test_reject_by_threshold():
    assert all(
        outliers.reject_by_threshold(pd.Series([1000, 1001, 999, 2000]), 5)
        == [False, False, False, True]
    )


def test_reject_by_threshold_with_ref_value():
    assert all(
        outliers.reject_by_threshold(
            pd.Series([1000, 1001, 999, 1010]), threshold=5, g_true=1010
        )
        == [True, True, True, False]
    )


def test_guess_mean_and_std():
    np.random.seed(0)
    n = 100
    ser = pd.Series(
        np.random.randn(n), index=pd.date_range("2024-01-01", freq="1s", periods=n)
    )
    mean, std = outliers.guess_mean_and_std(ser)
    assert mean == pytest.approx(0.03, abs=0.01)
    assert std == pytest.approx(1.002, abs=0.001)


def test_reject_by_sigma_threshold():
    np.random.seed(0)
    n = 100
    ser = pd.Series(
        np.random.randn(n), index=pd.date_range("2024-01-01", freq="1s", periods=n)
    )
    ser.iloc[30] += 20
    is_outlier = pd.Series(False, index=ser.index)
    is_outlier.iloc[30] = True
    assert all(outliers.reject_by_sigma_threshold(ser, sigma_threshold=3) == is_outlier)


def test_reject_neighbors():
    ser = pd.Series([False] * 7)
    ser.iloc[3] = True
    assert all(
        outliers.reject_neighbors(ser, num=2)
        == [False, True, True, True, True, True, False]
    )


def test_get_outlier_segments():
    is_outlier = pd.Series(
        False, index=pd.date_range("2024-01-01", freq="1s", periods=50)
    )
    is_outlier.iloc[10:20] = True
    is_outlier.iloc[30:40] = True
    assert outliers.get_outlier_segments(is_outlier) == [
        (pd.Timestamp("2024-01-01 00:00:10"), pd.Timestamp("2024-01-01 00:00:20")),
        (pd.Timestamp("2024-01-01 00:00:30"), pd.Timestamp("2024-01-01 00:00:40")),
    ]


def test_join_close_segments():
    is_outlier = pd.Series(
        False, index=pd.date_range("2024-01-01 00:00", "2024-01-01 00:05", freq="10s")
    )
    # Mark two segments with 2 min gap
    is_outlier.loc["2024-01-01 00:00:00":"2024-01-01 00:01:00"] = True
    is_outlier.loc["2024-01-01 00:03:00":"2024-01-01 00:04:00"] = True
    # Samples rejected because min_gap is larger than outlier gap
    is_gap = outliers.join_close_segments(is_outlier, min_gap="2min")
    assert all(is_gap.loc["2024-01-01 00:02:10":"2024-01-01 00:02:50"])
    # Gap is accepted
    is_gap = outliers.join_close_segments(is_outlier, min_gap="1min")
    assert not any(is_gap.loc["2024-01-01 00:01:10":"2024-01-01 00:02:50"])
