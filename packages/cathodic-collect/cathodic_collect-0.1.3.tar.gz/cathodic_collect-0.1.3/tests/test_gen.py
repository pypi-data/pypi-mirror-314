import typing as t
from pathlib import Path

from cathodic_collect import gen


def test_gen_meta(resource_folder: Path):
    work_dir = resource_folder / "2024-12-11-test"

    class MockStageFileReader(gen.device.StageFileReader):
        def get_workdir(self) -> Path:
            return work_dir

        def read_stage(self, stage_id: int, file_id: int, ctype: t.Literal["ac", "dc"]):
            return self.get_workdir() / f"result_{ctype}_{file_id}_{stage_id}.csv"

    g = gen.GenerateMeta(work_dir)
    g.set_stage_file_reader(MockStageFileReader())
    meta = g.generate()
    assert meta.header.project_name == "test"
    assert meta.header.file_num == 2
