import pathlib

import yaml
from cathodic_report.wordfile import forms
from pydantic import BaseModel


class ExtendedSumamryTable(forms.SummaryForm):
    is_protect: bool


class SimpleMeta(BaseModel):
    """This meta is created for before computing ."""

    has_ac: bool
    has_dc: bool
    header: forms.ReportForm.ReportHeader


class Meta(SimpleMeta):
    summary_table: list[ExtendedSumamryTable]

    @classmethod
    def read_meta(cls, base_dir: pathlib.Path):
        assert base_dir.exists(), "base_dir not exists"
        assert (base_dir / "meta.yml").exists(), "meta.yml not exists"
        with open(base_dir / "meta.yml", "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        return Meta.model_validate(meta)
