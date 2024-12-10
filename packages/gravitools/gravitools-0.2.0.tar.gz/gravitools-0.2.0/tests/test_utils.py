import datetime
import pathlib
import zipfile

import numpy as np
import pandas as pd
import pytest

from gravitools.utils import (
    files_in_path,
    interpolate_time_series,
    is_date,
    merge_dicts,
    sort_paths_numerically,
    to_path,
)


def test_interpolate_time_series():
    index = pd.date_range("2024-01-01 12", "2024-01-01 14", freq="1h")
    data = pd.Series(np.arange(len(index)), index=index)
    new_index = pd.date_range("2024-01-01 11", "2024-01-01 15", freq="30min")
    interpolated_data = interpolate_time_series(data, new_index)
    assert all(interpolated_data.index == new_index)
    assert np.array_equal(
        interpolated_data.values,
        [float("nan"), float("nan"), 0, 0.5, 1, 1.5, 2, float("nan"), float("nan")],
        equal_nan=True,
    )


def test_to_path_str():
    assert to_path("path/to/file.txt") == pathlib.PosixPath("path/to/file.txt")


def test_to_path_path():
    assert to_path(pathlib.Path("path/to/file.txt")) == pathlib.PosixPath(
        "path/to/file.txt"
    )


@pytest.fixture(scope="session")
def archive(tmpdir_factory):
    tmp_path = tmpdir_factory.mktemp("to_path")
    archive = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive, "w") as z:
        with z.open("testfile.txt", "w") as f:
            f.write(b"")
    return archive


def test_to_path_zip_from_str(archive):
    # str to archive.zip
    p = to_path(str(archive))
    assert isinstance(p, zipfile.Path)
    assert str(p) == str(archive) + "/"


def test_to_path_zip_from_path(archive):
    # pathlib.Path to archive.zip
    p = to_path(archive)
    assert p.root.filename == str(archive)
    assert p.at == ""


def test_to_path_within_zip_from_path(archive):
    # pathlib.Path to archive.zip/testfile.txt
    p = to_path(archive / "testfile.txt")
    assert p.root.filename == str(archive)
    assert p.at == "testfile.txt"


def test_to_path_within_zip_from_str(archive):
    # str to archive.zip/testfile.txt
    p = to_path(str(archive / "testfile.txt"))
    assert p.at == "testfile.txt"


def test_to_path_within_zip_from_zippath(archive):
    # zipfile.Path to archive.zip/testfile.txt
    z = zipfile.Path(archive, at="testfile.txt")
    assert to_path(z) == z


def test_merge_dicts_simple():
    a = {"a": 1, "b": 2}
    b = {"b": 3, "c": 4}
    c = merge_dicts(a, b)
    assert c == {"a": 1, "b": 3, "c": 4}
    # Check that inputs were not changed
    assert a == {"a": 1, "b": 2}
    assert b == {"b": 3, "c": 4}


def test_merge_dicts_one_nested():
    a = {"a": 2}
    b = {"a": {"x": 5}}
    c = merge_dicts(a, b)
    assert c == {"a": {"x": 5}}
    # Check that inputs were not changed
    assert a == {"a": 2}
    assert b == {"a": {"x": 5}}


def test_merge_dicts_both_nested():
    a = {"a": {"x": 5}}
    b = {"a": {"y": 6}}
    c = merge_dicts(a, b)
    assert c == {"a": {"x": 5, "y": 6}}
    # Check that inputs were not changed
    assert a == {"a": {"x": 5}}
    assert b == {"a": {"y": 6}}


@pytest.mark.parametrize(
    "text",
    [
        "2024-01-02",
        "2024-01-02 12:34",
        datetime.date(2023, 1, 2),
        datetime.datetime(2023, 1, 2, 12, 34, 56),
    ],
)
def test_is_date(text):
    assert is_date(text)


@pytest.mark.parametrize(
    "text",
    [
        "20240102",
        "2024-01-02 12:34:56",
        "not a date",
        "2024-01-xy",
        "2024-01",
    ],
)
def test_is_date_invalid(text):
    assert not is_date(text)


def test_sort_paths_numerically_one():
    path = "capture_20200123_123456_raw.csv"
    assert sort_paths_numerically([path]) == [path]


def test_files_in_path_with_dir(tmp_path):
    # Create test files
    testfiles = [tmp_path / f"testfile{i}.txt" for i in range(3)]
    for path in testfiles:
        path.touch()
    assert isinstance(tmp_path, pathlib.Path)
    assert sorted(files_in_path(tmp_path)) == testfiles


def test_files_in_path_with_zip_at_root(tmp_path):
    # Create zip-archive with files at root
    archive_path = tmp_path / "archive.zip"
    testfiles = [f"testfile{i}.txt" for i in range(1)]
    with zipfile.ZipFile(archive_path, mode="w") as z:
        for filename in testfiles:
            z.writestr(filename, data="")

    expected = [zipfile.Path(archive_path, path) for path in testfiles]
    result = files_in_path(archive_path)

    # Compare as string because direct equality of zipfile.Path does not work
    # in this case.
    assert sorted(map(str, result)) == sorted(map(str, expected))


def test_files_in_path_with_zip_at_subfolder(tmp_path):
    # Create zip-archive with files inside subfolder
    archive_path = tmp_path / "archive.zip"
    testfiles = [f"subfolder/testfile{i}.txt" for i in range(3)]
    with zipfile.ZipFile(archive_path, mode="w") as z:
        for filename in testfiles:
            z.writestr(filename, data="")
        # This filde should NOT be listed by files_in_path()
        z.writestr("outside_subfolder.txt", data="")

    expected = [zipfile.Path(archive_path, path) for path in testfiles]

    # files_in_path() should handle missing '/' at the end
    path = zipfile.Path(archive_path, "subfolder")
    result = files_in_path(path)

    # Compare as string because direct equality of zipfile.Path does not work
    # in this case.
    assert sorted(map(str, result)) == sorted(map(str, expected))
