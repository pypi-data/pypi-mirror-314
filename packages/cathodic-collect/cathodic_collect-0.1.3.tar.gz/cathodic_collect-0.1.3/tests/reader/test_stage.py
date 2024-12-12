import pandas as pd
import pytest

from cathodic_collect.reader.graph import Stage2


@pytest.mark.parametrize("filename", ["out2-ac.csv", "out2-dc.csv"])
def test_stage2_file(base_dir, filename, df_reader):
    assert set(Stage2.header) <= set(
        pd.read_csv(base_dir / filename, encoding="gbk").keys()
    )
    Stage2(df_reader.read_csv(base_dir / filename))
