import abc
import typing as t
from pathlib import Path

import yaml
from cathodic_report import graph
from cathodic_report.wordfile import forms

from .forms import Meta
from .reader import graph as graph_reader
from .reader import device as device_reader


class Collect(abc.ABC):
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.meta = self.read_meta()
        self.init = False

    def add_graph_reader(self, graph_reader: graph_reader.GraphReader):
        self.graph_reader = graph_reader

    def add_device_reader(self, device_reader_cls: t.Type[device_reader.DeviceReader]):
        self.device_reader = device_reader_cls(self.meta)

    def read_meta(self) -> Meta:
        return Meta.read_meta(self.base_dir)

    def get_header(self) -> forms.ReportForm.ReportHeader:
        return self.meta.header

    def get_summary_table(self) -> list[forms.SummaryForm]:
        return self.meta.summary_table

    def get_circle_graph(self) -> list[forms.graph.CircleGraph]:
        tables = self.get_summary_table()

        maps = {
            "高": graph.JudgeLevel.high,
            "中": graph.JudgeLevel.mid,
            "低": graph.JudgeLevel.low,
        }

        judge_result_ac = [maps[row.ac_judge_result] for row in tables]
        judge_result_dc = [maps[row.dc_judge_result] for row in tables]
        return [
            forms.graph.CircleGraph(types="ac", judge_result_data=judge_result_ac),
            forms.graph.CircleGraph(types="dc", judge_result_data=judge_result_dc),
        ]

    def get_graph_data(self) -> forms.graph.GraphData:
        return self.graph_reader.read_graph_data(
            circle_graphs=self.get_circle_graph(),
        )

    def collect(self) -> forms.ReportForm:
        return forms.ReportForm(
            header=self.get_header(),
            summary_table=self.get_summary_table(),
            graph_data=self.get_graph_data(),
            device_info=[self.device_reader.read_device(file_id=file_id) for file_id in range(1, self.meta.header.file_num + 1)],
        )
