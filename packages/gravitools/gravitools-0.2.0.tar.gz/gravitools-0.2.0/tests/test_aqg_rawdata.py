from pathlib import Path

import pandas as pd
import pytest

from gravitools.aqg import read_aqg_raw_dataset
from gravitools.aqg.rawdata import AQGRawData
from gravitools.quantity import Gradient


def test_read_aqg_raw_dataset():
    data = Path(__file__).parent.parent / "data"
    path = data / "20240620_163341.zip"
    raw = read_aqg_raw_dataset(path)
    assert raw.point == "CA"
    assert raw.orientation is None
    assert raw.meter == "AQG-B02"
    assert raw.start_time == pd.Timestamp("2024-06-20 16:33:42+0000")
    assert raw.metadata["reference_height"] == "0.6500 m"
    assert raw.metadata["dg_syst"] == "14.0 nm/s²"
    assert raw.const_corrections == {"dg_syst": 14}
    assert raw.metadata["vgg"] == "-3287.0 nm/s²/m"
    raw.process(
        recalculate_dg_polar=False,
        operator="John Doe",
        dg_syst=123,
        syst_uncertainty="101 nm/s²",
        pressure_admittance=-3,
        tilt_offset=(-2.4269e-6, -5.526e-6),
        change_tilt_offset=(5.65e-5, -4.68e-5),
        comment="This is a comment",
        outlier_ranges={
            "2023-02-16 16:40:00 .. 2023-02-16 16:45:00": {
                "comment": "Reason for outlier",
            }
        },
        point="WET_EA",
        vgg=-3000,
        station_height_difference=0.001,
    )

    dataset = raw.to_dataset()
    assert dataset.point == "WET_EA"
    assert dataset.metadata["vgg"] == "-3000.0 nm/s²/m"
    assert dataset.vgg == Gradient(-3000)
    assert dataset.h == 0.651
    assert dataset.comment == "This is a comment"
    assert dataset.metadata["dg_syst"] == "123.0 nm/s²"
    assert dataset.metadata["syst_uncertainty"] == "101.0 nm/s²"
    assert raw.pressure_admittance == -3
    assert dataset.metadata["operator"] == "John Doe"
    assert raw.metadata["reference_height"] == "0.6510 m"
    assert "station_height_difference" not in dataset.metadata
    assert "outlier_ranges" not in dataset.metadata
    assert raw.tilt_offset == (5.65e-5, -4.68e-5)
    assert dataset.metadata["tilt_offset_x"] == "56.5e-6 rad"
    assert dataset.metadata["tilt_offset_y"] == "-46.8e-6 rad"
    assert dataset.mean(h=None).height == dataset.h


def test_aqg_rawdata_set_pressure_admittance():
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="DATASET")
    assert "pressure_admittance" not in raw.metadata
    raw.set_pressure_admittance(-3)
    assert raw.metadata["pressure_admittance"] == "-3.00 nm/s²/hPa"
    raw.set_pressure_admittance("-2.9 nm/s²/hPa")
    assert raw.metadata["pressure_admittance"] == "-2.90 nm/s²/hPa"


@pytest.mark.parametrize(
    "key,value,result",
    [
        ("dg_syst", "12.34 nm/s²", "12.3 nm/s²"),
        ("dg_syst", "1.234 µGal", "12.3 nm/s²"),
        ("dg_syst", 12.34, "12.3 nm/s²"),
        ("pressure_admittance", "-0.3 µGal/hPa", "-3.00 nm/s²/hPa"),
        ("pressure_admittance", -3, "-3.00 nm/s²/hPa"),
        ("vgg", "-300 µGal/m", "-3000.0 nm/s²/m"),
        ("vgg", -3000, "-3000.0 nm/s²/m"),
    ],
)
def test_aqg_rawdata_replace_metadata(key, value, result):
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="")
    raw.replace_metadata(**{key: value})
    assert raw.metadata[key] == result


@pytest.mark.parametrize(
    "tilt_offset",
    [
        (123e-6, 1234e-6),
        "123e-6, 1234e-6",
        ("123e-6 rad", "1234e-6 rad"),
        "123e-6 rad, 1234e-6 rad",
    ],
)
def test_aqg_rawdata_replace_metadata_tilt_offset(tilt_offset):
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="")
    assert "tilt_offset_x" not in raw.metadata
    assert "tilt_offset_y" not in raw.metadata
    raw.replace_metadata(tilt_offset=tilt_offset)
    assert raw.metadata["tilt_offset_x"] == "123.0e-6 rad"
    assert raw.metadata["tilt_offset_y"] == "1234.0e-6 rad"


def test_aqg_rawdata_replace_metadata_orientation():
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="")
    assert "orientation" not in raw.metadata
    raw.replace_metadata(orientation=180)
    assert raw.metadata["orientation"] == "180.0°"


def test_aqg_rawdata_replace_metadata_default_orientation():
    raw = AQGRawData(pd.DataFrame(), metadata={"orientation": "180.0°"}, name="")

    # Orientation already defined (nothing to do)
    raw.replace_metadata(default_orientation=0)
    assert raw.metadata["orientation"] == "180.0°"

    # Orientation unknown, use default
    raw.metadata["orientation"] = None
    raw.replace_metadata(default_orientation=0)
    assert raw.metadata["orientation"] == "0.0°"

    # Orientation unknown, but configured
    raw.metadata["orientation"] = None
    raw.replace_metadata(default_orientation=0, orientation=180)
    assert raw.metadata["orientation"] == "180.0°"


def test_aqg_rawdata_replace_metadata_dg_const(monkeypatch):
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="")

    def set_const_correction(self, name, value):
        assert name == "dg_custom"
        assert value == 123.4
        self.metadata[name] = "123.4 nm/s²"

    monkeypatch.setattr(
        "gravitools.aqg.rawdata.AQGRawData.set_const_correction", set_const_correction
    )

    assert "dg_custom" not in raw.metadata
    raw.replace_metadata(dg_custom=123.4)
    assert raw.metadata["dg_custom"] == "123.4 nm/s²"


@pytest.mark.parametrize(
    "name,value,key,result",
    [
        ("test", 123.45, "dg_test", "123.5 nm/s²"),
        ("dg_test", 123.45, "dg_test", "123.5 nm/s²"),
        ("dg_test", "123.45 nm/s²", "dg_test", "123.5 nm/s²"),
        ("dg_test", "12.345 µGal", "dg_test", "123.5 nm/s²"),
    ],
)
def test_aqg_rawdata_set_const_correction(name, value, key, result):
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="")
    assert key not in raw.metadata
    raw.set_const_correction(name, value)
    assert raw.metadata[key] == result


def test_aqg_rawdata_orientation():
    raw = AQGRawData(pd.DataFrame(), metadata={"orientation": "180.0°"}, name="")
    assert raw.orientation == 180.0


def test_aqg_rawdata_tilt_offset():
    metadata = {
        "tilt_offset_x": "123e-6 rad",
        "tilt_offset_y": "234e-6 rad",
    }
    raw = AQGRawData(pd.DataFrame(), metadata=metadata, name="")
    assert raw.tilt_offset == (123e-6, 234e-6)


def test_aqg_rawdata_recalculate_tilt(monkeypatch):
    metadata = {
        "tilt_offset_x": "123e-6 rad",
        "tilt_offset_y": "234e-6 rad",
    }
    df = pd.DataFrame(
        {
            "x_tilt": [0.0],
            "y_tilt": [0.0],
            "is_outlider": [False],
        },
        index=[pd.Timestamp("2024-01-01")],
    )
    raw = AQGRawData(df, metadata=metadata, name="")

    def do_nothing(self):
        return

    monkeypatch.setattr(
        "gravitools.aqg.rawdata.AQGRawData.calculate_dg_tilt", do_nothing
    )

    dx, dy = 10e-6, 20e-6
    new_offset = 123e-6 + dx, 234e-6 + dy
    raw.recalculate_tilt(new_offset)
    assert raw.tilt_offset == new_offset
    assert raw.df.x_tilt.iloc[0] == pytest.approx(-dx, abs=1e-8)
    assert raw.df.y_tilt.iloc[0] == pytest.approx(-dy, abs=1e-8)


def test_aqg_rawdata_recalculate_tilt_no_tilt_offset():
    raw = AQGRawData(pd.DataFrame(), metadata={}, name="")
    assert "tilt_offset_x" not in raw.metadata
    assert "tilt_offset_y" not in raw.metadata
    with pytest.raises(ValueError) as exc:
        raw.recalculate_tilt((0.123, 1.234))
    assert "Original tilt offset is unknown" in str(exc.value)
