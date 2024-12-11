from pathlib import Path

from cathodic_report.wordfile import forms as rforms

from cathodic_collect.forms import Meta
from cathodic_collect.myreader import get_reader


def get_device_form(base_dir: Path, file_id: int) -> rforms.DeviceForm:
    meta = Meta.read_meta(base_dir)
    Reader = get_reader(base_dir)
    reader = Reader(meta)
    return reader.get_device_form(file_id=file_id)
