import typing as t
from pathlib import Path

import pandas as pd
import yaml

from . import forms
from .reader import device, dfreader, stage


class GenerateMeta:
    """from simpleMeta to meta"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.df_reader = dfreader.DFReader()

    def set_stage_file_reader(self, stage_file_reader: device.StageFileReader):
        self.stage_file_reader = stage_file_reader

    def read_stage(
        self, stage_id: int, file_id: int, ctype: t.Literal["ac", "dc"]
    ) -> pd.DataFrame:
        return self.df_reader.read_csv(
            self.stage_file_reader.read_stage(stage_id, file_id, ctype)
        )

    def generate(self) -> forms.Meta:
        with open(self.base_dir / "simple_meta.yml", "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        simple_meta = forms.SimpleMeta.model_validate(meta)

        tables = []
        extended_tables = []
        for table in simple_meta.summary_table:
            tables.append(table.model_dump())
            if simple_meta.has_ac:
                stage3 = stage.Stage3(self.read_stage(3, table.id, ctype="ac"))
                ac_result = stage3.get_result()
            if simple_meta.has_dc:
                stage3 = stage.Stage3(self.read_stage(3, table.id, ctype="dc"))
                dc_result = stage3.get_result()
            table_dict = table.model_dump()
            table_dict["ac_judge_result"] = ac_result
            table_dict["dc_judge_result"] = dc_result
            extended_tables.append(table_dict)

        summary_table = [
            forms.ExtendedSummaryTable.model_validate(extended_table)
            for extended_table in extended_tables
        ]

        return forms.Meta(
            has_ac=simple_meta.has_ac,
            has_dc=simple_meta.has_dc,
            header=simple_meta.header,
            summary_table=summary_table,
        )
