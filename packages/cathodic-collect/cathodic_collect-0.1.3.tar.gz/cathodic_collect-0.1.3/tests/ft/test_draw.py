from pathlib import Path

from . import s
from .report import MyReport


def test_get_graph_for_file(base_dir: Path, tmp_folder: s.Path):
    """
    尝试采用简单的方式进行绘图
    """
    res = s.get_tsdata_from_file(base_dir, 1)
    MyReport(workdir=tmp_folder).render_device_graph(res)
