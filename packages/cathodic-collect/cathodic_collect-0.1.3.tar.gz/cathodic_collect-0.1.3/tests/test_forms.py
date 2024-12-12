from pathlib import Path

from cathodic_collect.forms import Meta


def test_read_meta(base_dir: Path):
    meta = Meta.read_meta(base_dir)
    assert meta.has_ac
    assert meta.has_dc
    assert meta.header
    assert meta.summary_table
