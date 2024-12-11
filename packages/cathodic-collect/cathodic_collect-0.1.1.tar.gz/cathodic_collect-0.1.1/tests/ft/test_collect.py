from pathlib import Path

import pytest
from cathodic_report.report import Report
from cathodic_report.wordfile import forms as rforms

from cathodic_collect.collect import Collect
from cathodic_collect.reader import graph, device
from cathodic_collect import myreader


# 定义一个简单的 Reader，让 distance 以及 resistivity 全部为返回 100
class GraphReader(graph.GraphReader):
    def get_distance(self, file_id: int) -> float:
        return 100

    def get_resistivity(self, file_id: int) -> float:
        return 100

    def get_filename(self) -> Path:
        """获取文件名称，类型为二级文件"""
        file = global_files["default"]  # noqa
        assert file.exists(), f"文件 {file} 不存在"
        return file


global_files = {"default": Path("out2-ac.csv")}


@pytest.fixture
def collect(sample_base_dir: Path):
    return Collect(base_dir=sample_base_dir)

@pytest.fixture
def sample_base_dir(resource_folder: Path):
    return resource_folder / '2024-12-11-test'


def test_collect(collect: Collect, sample_base_dir: Path):
    global_files["default"] = sample_base_dir / "output_ac.csv"
    reader = GraphReader(10)
    collect.add_graph_reader(reader)

    DeviceReader = myreader.get_reader(sample_base_dir)
    collect.add_device_reader(DeviceReader)

    report = collect.collect()
    assert isinstance(report, rforms.ReportForm)
