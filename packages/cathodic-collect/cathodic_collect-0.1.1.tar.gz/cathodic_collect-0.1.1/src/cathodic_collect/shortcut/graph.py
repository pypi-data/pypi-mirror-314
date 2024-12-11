from pathlib import Path

from cathodic_report.wordfile import forms as rforms

from cathodic_collect.forms import Meta
from cathodic_collect.myreader import get_reader


def get_tsdata_from_file(base_dir: Path, file_id: int) -> rforms.DeviceTimeSeries:
    meta = Meta.read_meta(base_dir)
    Reader = get_reader(base_dir)
    reader = Reader(meta)

    res = reader.get_graph_data(file_id=file_id)
    return res
