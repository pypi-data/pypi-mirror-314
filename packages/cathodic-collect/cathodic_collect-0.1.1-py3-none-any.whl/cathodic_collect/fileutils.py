# merge stage-2 files

from pathlib import Path as _p

import pandas as pd

from .utils import get_output_file_encode

encoding = get_output_file_encode()


def read_file_list(file_list: list[_p]) -> list[pd.DataFrame]:
    for file in file_list:
        assert file.exists(), f"文件不存在: {file}"

    return [pd.read_csv(file, encoding=encoding) for file in file_list]


def merge_stage_2_files(file_list: list[pd.DataFrame], output_path: _p) -> pd.DataFrame:
    """合并 stage-2 文件"""
    df = pd.concat(file_list)
    df.to_csv(output_path, index=False, encoding=encoding)
    return df
