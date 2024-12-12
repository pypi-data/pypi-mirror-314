from pathlib import Path
from pathlib import Path as _p
from typing import Literal

from cathodic_collect import fileutils


def test_generate_merged_file(sample_base_dir: Path):
    class Real(fileutils.GenerateFileList):
        def get_basedir(self) -> fileutils._p:
            return sample_base_dir

        def get_stage_file(
            self, stage: int, file_id: int, ctype: Literal["ac"] | Literal["dc"]
        ) -> Path:
            return self.get_basedir() / f"result_{ctype}_{file_id}_{stage}.csv"

        def get_merge_filepath(self, ctype: Literal["ac"] | Literal["dc"]) -> Path:
            return self.get_basedir() / f"output_2_{ctype}.csv"

    g = Real()
    flist = g.generate_file_list(2, "ac")
    assert len(flist) == 2

    g.generate_merged_file(2)

    for ctype in ["ac", "dc"]:
        assert sample_base_dir / f"output_2_{ctype}.csv"
