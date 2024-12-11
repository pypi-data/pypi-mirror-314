from pathlib import Path

import yaml

from cathodic_collect.forms import Meta
from cathodic_collect.myreader import get_reader


def test_device_graph(base_dir: Path, tmp_folder):
    meta = Meta.read_meta(base_dir)
    Reader = get_reader(base_dir)
    reader = Reader(meta)

    res = reader.get_graph_data(file_id=1)

    def write_to_yaml():
        # cost a long time.
        with open(tmp_folder / "res.yaml", "w") as f:
            yaml.dump(res.model_dump(), f)

    # write_to_yaml()
