import numpy as np
import pandas as pd
import pytest

from gravitools.quantity import Gradient
from gravitools.timeseries import GravityTimeSeries, TimeSeries


@pytest.fixture
def data():
    np.random.seed(0)
    n = 100000
    dr = pd.date_range("2020-01-01", freq="1s", periods=n)
    y = 9.8e9 + 100 * np.random.randn(n)
    return pd.Series(y, index=dr, name="demodata")


@pytest.fixture
def timeseries(data):
    return TimeSeries(data)


@pytest.fixture
def gravity_timeseries(data):
    return GravityTimeSeries(data, height=1.25)


def test_time_series_has_error(timeseries):
    assert not timeseries.has_error
    timeseries.df["y_err"] = 10
    assert timeseries.has_error


def test_time_series_mean(timeseries):
    mu, std, sem = timeseries.mean()
    assert mu == pytest.approx(9800000000.16, abs=0.01)
    assert std == pytest.approx(99.73, abs=0.01)
    assert sem == pytest.approx(0.3154, abs=0.0001)


def test_time_series_std(timeseries):
    std = timeseries.std()
    assert std == pytest.approx(99.73, abs=0.01)


def test_time_series_adev(timeseries):
    adev = timeseries.adev()
    assert adev[1] == pytest.approx(99.61, abs=0.01)
    assert adev[39069] == pytest.approx(0.339855, abs=1e-5)


def test_time_series_resample(timeseries):
    ts = timeseries.resample("1min")
    assert len(ts.y) == 1668
    assert ts.has_error
    mu, std, sem = ts.mean()
    assert mu == pytest.approx(9800000000.13, abs=0.01)
    assert std == pytest.approx(13.20, abs=0.01)
    assert sem == pytest.approx(0.3291, abs=0.0001)


def test_gravity_time_series_mean_std(gravity_timeseries):
    g_mean = gravity_timeseries.mean_std()
    assert g_mean.value == pytest.approx(9800000000.16, abs=0.01)
    assert g_mean.error == pytest.approx(99.73, abs=0.01)
    assert g_mean.height == 1.25


def test_gravity_time_series_transfer(data):
    vgg = Gradient(-3000)
    g = GravityTimeSeries(data, height=1.25, vgg=vgg)
    g2 = g.transfer(0)
    dg = 3000 * 1.25
    assert g2.mean_std().value == g.mean_std().value + dg


def test_gravity_time_series_transfer_no_height(data):
    vgg = Gradient(-3000)
    with pytest.raises(ValueError) as exc:
        GravityTimeSeries(data, vgg=vgg).transfer(0)
    assert "height" in str(exc.value)


def test_gravity_time_series_transfer_no_vgg(data):
    with pytest.raises(ValueError) as exc:
        GravityTimeSeries(data, height=1.25).transfer(0)
    assert "gradient" in str(exc.value)
