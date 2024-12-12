from pathlib import Path

from cathodic_report.wordfile import forms as rforms

from cathodic_collect.reader import graph


class GraphReader(graph.GraphReader):
    def get_distance(self, file_id: int) -> float:
        return 100

    def get_resistivity(self, file_id: int) -> float:
        return 100

    def get_filename(self) -> Path:
        """获取文件名称，类型为二级文件"""
        return global_files["default"]  # noqa


global_files = {
    "default": Path("out2-ac.csv"),
}


def test_graph(base_dir: Path):
    reader = GraphReader(file_num=1)
    global_files["default"] = base_dir / "out2-ac.csv"
    circle_graphs = [
        rforms.graph.CircleGraph(types="ac", judge_result_data=[1, 2, 3]),
        rforms.graph.CircleGraph(types="dc", judge_result_data=[1, 2, 3]),
    ]
    reader.read_graph_data(circle_graphs=circle_graphs)
