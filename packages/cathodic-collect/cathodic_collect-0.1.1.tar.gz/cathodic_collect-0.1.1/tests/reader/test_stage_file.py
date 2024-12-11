import typing as t
from pathlib import Path

from cathodic_collect import myreader as myreader
from cathodic_collect.forms import Meta
from cathodic_collect.reader import device


def test_device_reader(base_dir: Path):
    meta = Meta.read_meta(base_dir)
    DeviceReader = myreader.get_reader(base_dir)
    reader = DeviceReader(meta)
    file = reader.read_stage(1, 1, "ac")

    assert file.exists()
    assert file.is_file()
