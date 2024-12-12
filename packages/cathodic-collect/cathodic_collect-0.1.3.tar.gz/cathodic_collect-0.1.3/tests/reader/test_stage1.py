import pytest

from cathodic_collect.reader.stage import Stage1


@pytest.mark.parametrize("filename", ["out1-ac.csv", "out1-dc.csv"])
def test_stage1(base_dir, filename, df_reader):
    s1 = Stage1(df_reader.read_csv(base_dir / filename))
    assert not s1.df.empty

    start, end = s1.get_start_end()
    assert end > start

    assert s1.total_time() < 24 * 2
