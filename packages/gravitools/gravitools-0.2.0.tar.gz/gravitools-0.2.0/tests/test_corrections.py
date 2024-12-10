import numpy as np
import pandas as pd
import pytest

from gravitools import corrections
from gravitools.aqg.tilt import TILT_FOR_1_UGAL


def test_nominal_pressure():
    assert corrections.nominal_pressure(0) == pytest.approx(1013.25, abs=0.01)
    assert corrections.nominal_pressure(100) == pytest.approx(1001.29, abs=0.01)
    assert corrections.nominal_pressure(200) == pytest.approx(989.45, abs=0.01)
    assert corrections.nominal_pressure(500) == pytest.approx(954.61, abs=0.01)
    assert corrections.nominal_pressure(1000) == pytest.approx(898.75, abs=0.01)
    assert corrections.nominal_pressure(2000) == pytest.approx(794.95, abs=0.01)


def test_pressure_correction():
    assert corrections.pressure_correction(1000.0, altitude=0) == 39.75


@pytest.mark.parametrize(
    "x,y,dg",
    [
        [15e-6, 0, -1.1],
        [30e-6, 0, -4.41],
        [3000e-6, 0, -44100.17],
        [0, 15e-6, -1.1],
        [0, 30e-6, -4.41],
        [TILT_FOR_1_UGAL, 0, -10],
        # Test type casting to float64
        [np.array([15e-6], dtype="float32"), 0, -1.1],
        [0, np.array([15e-6], dtype="float32"), -1.1],
    ],
)
def test_tilt_correction(x, y, dg):
    assert corrections.tilt_correction(9.8e9, x, y) == pytest.approx(dg, abs=0.01)


def test_polar_motion_correction():
    lat, lon = 49.14490, 12.88025  # Wettzell
    x, y = 0.054645, 0.276985  # 2022-01-01
    assert corrections.polar_motion_correction(x, y, lat, lon) == pytest.approx(
        -1.60, abs=0.01
    )


def test_dg_polar():
    lat, lon = 49.14490, 12.88025  # Wettzell
    eop = pd.DataFrame(
        {
            "x": [0.076577, 0.074635],
            "y": [0.282336, 0.282712],
            "type": ["final", "final"],
        },
        index=pd.to_datetime(["2020-01-01", "2020-01-02"]),
    )
    index = pd.date_range("2020-01-01", periods=5, freq="6h")
    dg = corrections.dg_polar(index, lat, lon, eop)
    assert dg.iloc[0] == pytest.approx(2.218, abs=0.001)
    assert dg.iloc[1] == pytest.approx(2.124, abs=0.001)
    assert dg.iloc[2] == pytest.approx(2.031, abs=0.001)
    assert dg.iloc[3] == pytest.approx(1.938, abs=0.001)
    assert dg.iloc[4] == pytest.approx(1.844, abs=0.001)


def test_get_eop_data():
    corrections.eop_data = "TEST"
    assert corrections.get_eop_data() == "TEST"


def test_get_eop_data_read(monkeypatch):
    corrections.eop_data = None

    def mock_read_eop_data():
        return "TEST"

    monkeypatch.setattr(corrections, "read_eop_data", mock_read_eop_data)
    assert corrections.get_eop_data() == "TEST"


def test_update_eop_data(tmp_path, monkeypatch):
    path = tmp_path / "eop.csv"
    corrections.EOP_PATH = path

    def mock_download_file(url, path):
        assert url == corrections.EOP_URL
        path.write_text(
            """
            MJD;Year;Month;Day;Type;x_pole;sigma_x_pole;y_pole;sigma_y_pole
            58849;2020;01;01;final;0.076577;0.000032;0.282336;0.000027
            58850;2020;01;02;final;0.074635;0.000032;0.282712;0.000027
            """
        )

    monkeypatch.setattr(corrections, "_download_file", mock_download_file)
    eop = corrections.update_eop_data()
    assert all(eop["x"] == [0.076577, 0.074635])


def test_read_eop_data(tmp_path):
    path = tmp_path / "eop.csv"
    path.write_text(
        """
        MJD;Year;Month;Day;Type;x_pole;sigma_x_pole;y_pole;sigma_y_pole
        58849;2020;01;01;final;0.076577;0.000032;0.282336;0.000027
        58850;2020;01;02;final;0.074635;0.000032;0.282712;0.000027
        """
    )
    corrections.EOP_PATH = path
    eop = corrections.read_eop_data()
    assert all(eop["x"] == [0.076577, 0.074635])
    assert all(eop["y"] == [0.282336, 0.282712])
    assert all(eop["type"] == ["final", "final"])
