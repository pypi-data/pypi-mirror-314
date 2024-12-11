from pathlib import Path

from . import collect
from .reader import graph


def build_collect(base_dir: Path, reader: graph.GraphReader) -> collect.Collect:
    co = collect.Collect(base_dir)
    co.add_graph_reader(reader)
    return co
