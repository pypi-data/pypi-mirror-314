import numpy as np
import pandas as pd
import pytest

from gravitools.aqg.tilt import (
    TiltOffset,
    analyze_aqg_tilt_calibration,
    calculate_tilt_dataset_means,
    fit_model,
    perform_tilt_offset_fit,
)


def make_datapoints(tx, ty, g0):
    n = 5
    tilt_x = 1e-3 * np.linspace(-1, 1, n) + tx + 50e-6
    tilt_y = 1e-3 * np.linspace(-1, 1, n) + ty + 50e-6
    tilt = np.array(np.meshgrid(tilt_x, tilt_y)).reshape(2, n * n)
    g = fit_model(tilt, tx, ty, g0)
    return pd.DataFrame(
        dict(
            g=g,
            g_err=50 * np.ones(n * n),
            tilt_x=tilt[0],
            tilt_y=tilt[1],
        )
    )


def test_perform_tilt_offset_fit():
    tx = 1.234e-3
    ty = 0.345e-3
    g0 = 9.8e9
    datapoints = make_datapoints(tx, ty, g0)
    tilt_offset = perform_tilt_offset_fit(
        datapoints.tilt_x, datapoints.tilt_y, datapoints.g, datapoints.g_err
    )
    assert tilt_offset.x == pytest.approx(tx, abs=1e-7)
    assert 0 < tilt_offset.u_x < 1e-7
    assert tilt_offset.y == pytest.approx(ty, abs=1e-7)
    assert 0 < tilt_offset.u_y < 1e-7
    assert tilt_offset.g == pytest.approx(g0, abs=1e-2)
    assert tilt_offset.u_g == pytest.approx(0, abs=1e-2)


def test_analyze_tilt_calibration(monkeypatch):
    rawdata_paths = [1, 2, 3]
    cfg = {"param": "value"}
    datapoints = make_datapoints(0, 0, 9.8e9)
    result = TiltOffset(1, 2, 3, 4)

    def process(path, config):
        assert config == cfg

    def means(datasets):
        return datapoints

    def fit(tilt_x, tilt_y, g, g_err):
        return result

    monkeypatch.setattr("gravitools.aqg.tilt.process_aqg_raw_dataset", process)
    monkeypatch.setattr("gravitools.aqg.tilt.calculate_tilt_dataset_means", means)
    monkeypatch.setattr("gravitools.aqg.tilt.perform_tilt_offset_fit", fit)

    tilt_analysis = analyze_aqg_tilt_calibration(rawdata_paths, config=cfg, name="DEMO")
    assert tilt_analysis.datapoints is datapoints
    assert tilt_analysis.result is result
    assert tilt_analysis.name == "DEMO"
    assert tilt_analysis.datasets == 3 * [None]


def test_calculate_tilt_dataset_means():
    class MockTimeSeries:
        def __init__(self):
            self.y = pd.Series(np.linspace(-100, 100, 60) + 9.8e9)
            self.y.index = pd.date_range("2024-01-01", "2024-01-01 00:00:59", freq="1s")

        ## this function is copied from `gravitools.math.interval_means()`
        def resample(self, interval, min_count=None, name=None, err="sem"):

            # Shift interval such that index value is at the center (default is
            # beginning)
            offset = pd.tseries.frequencies.to_offset(interval) / 2

            name = "y"

            # Calculate interval means, SEM and sample count
            means = self.resample(interval, offset=offset).mean().to_frame(name)
            if err == "sem":
                means[name + "_err"] = self.resample(interval, offset=offset).sem()
            elif err == "std":
                means[name + "_err"] = self.resample(interval, offset=offset).std()
            else:
                raise ValueError(
                    f"Parameter 'err' should be 'sem' or 'std', but is {err!r}."
                )
            means[name + "_count"] = self.resample(interval, offset=offset).count()
            means.index += offset

    class MockDataset:
        name = "DEMO"
        num_drops = 5
        num_outliers = 1

        def get(self, column):
            return {
                "is_outlier": np.array(60 * [False]),
                "x_tilt": np.linspace(0, 1e-3, 60),
                "y_tilt": np.linspace(-1e-3, 0, 60),
                "dg_tilt": np.linspace(0, 50, 60),
            }[column]

        def full_g(self, incl_outliers):
            assert incl_outliers is False
            return MockTimeSeries()

    datasets = [MockDataset()]
    df = calculate_tilt_dataset_means(datasets)
    assert isinstance(df, pd.DataFrame)
    data = df.to_dict("records")[0]
    assert data["name"] == "DEMO"
    assert data["tilt_x"] == pytest.approx(0.5e-3)
    assert data["tilt_y"] == pytest.approx(-0.5e-3)
    assert data["g"] == pytest.approx(9.8e9 + 25, abs=0.01)
    assert data["g_err"] == pytest.approx(32.36, abs=0.01)
    assert data["valid_drops"] == 4
    assert data["total_drops"] == 5
