from pathlib import Path

from cathodic_collect import const
from cathodic_collect.reader import stage


def test_stage3(base_dir: Path, df_reader):
    s3 = stage.Stage3(df_reader.read_csv(base_dir / "result-dc.csv"))
    s3.set_df(s3.df[s3.df[const.TEST_ID_NAME] == "test"])
    print(s3.get_result())
