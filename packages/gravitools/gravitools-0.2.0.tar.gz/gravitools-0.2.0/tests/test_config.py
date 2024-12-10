import datetime

import pytest
import yaml

from gravitools.config import combine_dataset_config, select_date_config


@pytest.fixture
def date_config():
    return {
        "x": 1,  # global
        "2024-01-01": {"x": 2},
        "2024-02-01": {"x": 3},
    }


@pytest.mark.parametrize(
    "date,x",
    [
        (None, 1),
        ("2023-12-01", 1),
        ("2024-01-10", 2),
        ("2024-02-10", 3),
    ],
)
def test_select_date_config(date_config, date, x):
    assert select_date_config(date_config, date) == {"x": x}


def test_select_date_config_duplicate_date():
    with pytest.raises(ValueError):
        select_date_config(
            {"2023-01-01": {}, datetime.date(2023, 1, 1): {}}, "2023-01-02"
        )


def test_combine_config():
    assert combine_dataset_config(
        {
            "x": 5,
            "dataset A": {
                "z": 6,
                "y": 7,
                "corrections": {
                    "dg_syst": -123,
                },
            },
            "meter A": {
                "z": 1,
                "x": 3,
                "corrections": {
                    "syst_uncert": 101,
                    "dg_syst": 123,
                },
                "2023-12-01": {
                    "x": 20231201,
                },
                "2024-01-01": {
                    "x": 20240101,
                },
                "2024-02-01": {
                    "x": 20240201,
                },
            },
            "point A": {},
        },
        dataset="A",
        meter="A",
        date="2024-01-15",
    ) == {
        "x": 20240101,
        "y": 7,
        "z": 6,
        "corrections": {"dg_syst": -123, "syst_uncert": 101},
    }


def test_combine_config_precedence():
    # dataset params have highest priority
    assert combine_dataset_config(
        {
            "meter TEST": {"x": 1, "y": 1, "z": 1},
            "point TEST": {"x": 2, "y": 2},
            "dataset TEST": {"x": 3},
        },
        dataset="TEST",
        meter="TEST",
        point="TEST",
    ) == {"x": 3, "y": 2, "z": 1}


def test_combine_config_empty_param():
    assert combine_dataset_config(
        {
            "x": 1,
            "dataset TEST": {"x": None},
        },
        dataset="TEST",
    ) == {"x": None}


def test_config_from_yaml_with_date():
    text = """
    meter AQG-A02:
        '2022-01-01':
            dg_syst: 10 nm/s²
        2023-01-01:
            dg_syst: 20 nm/s²
    """
    config = yaml.load(text, Loader=yaml.CLoader)
    result = combine_dataset_config(config, meter="AQG-A02", date="2023-01-02")
    assert result == {"dg_syst": "20 nm/s²"}
