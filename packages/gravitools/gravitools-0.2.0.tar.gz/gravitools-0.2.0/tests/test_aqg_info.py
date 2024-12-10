from pathlib import Path

from gravitools.aqg.info import read_aqg_info


def test_read_aqg_info():
    data = Path(__file__).parent.parent / "data"
    path = (
        data
        / "20240620_163341.zip"
        / "20240620_163341"
        / "capture_20240620_163341.info"
    )
    metadata = read_aqg_info(path)
    assert metadata["point"] == "CA"
    assert metadata["orientation"] is None
