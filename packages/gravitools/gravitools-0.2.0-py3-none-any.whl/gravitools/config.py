from __future__ import annotations

from collections import Counter
import logging
import pathlib

import pandas as pd
import yaml

from gravitools.utils import is_date, merge_dicts, partition_dict

logger = logging.getLogger(__name__)


def read_config(path: str | pathlib.Path) -> dict:
    """Read a YAML config file

    Args:
        path:
            Path to a YAML config file.

    Returns:
        Dictionary of configuration parameters.
    """
    logger.debug(f"Read {path}")
    with open(path, encoding="utf-8") as f:
        config = yaml.load(f.read(), Loader=yaml.CLoader)
    return config


def select_date_config(config: dict, date: str | pd.Timestamp) -> dict:
    """Select configuration parameters for a measurement date

    Expects a dictionary of configuration parameters (`config`) that apply
    generally or are time-dependent. Time-dependent parameters should be
    grouped in a sub-dictionary with a key that denotes the starting date
    (identified by `is_date()`).

    For example:

        {
            'parameter1': 1,
            'parameter2': 2,
            '2020-01-01': {
                'parameter1: 2,
            },
            datetime.date(2021, 1, 1): {
                'parameter1: 3,
            },
        }

    Returns a merged dictionary of parameters that apply for the given `date`.

    Args:
        config:
            Configuration parameters.
        date:
            Measurement date.

    Returns:
        Dictionary of configuration parameters.

    Examples:
        >>> select_date_config({'x': 1, 'y': 2, '2020-01-01': {'x': 2}}, '2020-01-02')
        {'x': 2, 'y': 2}
    """
    date_configs, global_config = partition_dict(config, is_date)

    if date is None:
        return global_config

    date = pd.to_datetime(date, utc=True)

    # Keys in date_configs can be strings in date format, datetime.datetime or
    # datetime.date objects. Map them to a common type to make them comparable.
    timestamps = [pd.to_datetime(key, utc=True) for key in date_configs]

    # Throw an exception, if the same date occurs multiple times, e. g. as
    # string and datetime.date
    for timestamp, count in Counter(timestamps).items():
        if count >= 2:
            raise ValueError(f"Multiple configuration entries for {timestamp}")

    # Mapping of timestamp to keys in date_configs
    date_keys = dict(zip(timestamps, date_configs))

    # Find the newest configuration before the specified date
    for timestamp in sorted(date_keys, reverse=True):
        if timestamp <= date:
            key = date_keys[timestamp]
            return merge_dicts(global_config, date_configs[key])

    # Specified date is older than the oldest configuration
    return global_config


# TODO: There is a bug here. If the point name is overwritten, the 'point *'
# block will not be selected correctly.
def combine_dataset_config(
    config: dict,
    dataset: str = None,
    meter: str = None,
    point: str = None,
    date: str = None,
) -> dict:
    """Select configuration parameters for given dataset identifiers

    Args:
        config: Complete configuration parameters.
        dataset: Dataset identifier name.
        meter: Meter identifier.
        point: Point identifier.
        date: Measurement date.

    Returns:
        Configuration parameters specific to this dataset.
    """
    # Sorted by precedence (dataset overwrites point, overwrites meter configs)
    identifiers = {
        "meter": meter,
        "point": point,
        "dataset": dataset,
    }
    # Select global parameters
    dataset_config = {
        key: value
        for key, value in config.items()
        if not any(key.startswith(prefix + " ") for prefix in identifiers)
    }
    # Overwrite global parameters with more specific configurations
    for prefix, identifier in identifiers.items():
        if identifier is None:
            continue
        key = f"{prefix} {identifier}"
        if key not in config:
            continue
        identifier_config = config[key]
        # It doesn't make sense to have date config within a dataset config,
        # because the dataset has a fixed date
        if prefix in ["meter", "point"]:
            identifier_config = select_date_config(identifier_config, date=date)
        dataset_config = merge_dicts(dataset_config, identifier_config)
    return dataset_config
