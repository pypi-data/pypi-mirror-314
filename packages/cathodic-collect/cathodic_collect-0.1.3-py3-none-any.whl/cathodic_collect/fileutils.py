# merge stage-2 files

import abc
import typing as t
from pathlib import Path as _p

import pandas as pd

from .utils import get_output_file_encode

encoding = get_output_file_encode()


class GenerateFileList(abc.ABC):
    @abc.abstractmethod
    def get_basedir(self) -> _p:
        pass

    @abc.abstractmethod
    def get_stage_file(
        self, stage: int, file_id: int, ctype: t.Literal["ac", "dc"]
    ) -> _p:
        pass

    def generate_file_list(
        self, file_num: int, ctype: t.Literal["ac", "dc"]
    ) -> list[_p]:
        file_list = []
        for file_id in range(1, file_num + 1):
            file_list.append(self.get_stage_file(2, file_id, ctype))
        return file_list

    def get_merge_filepath(self, ctype: t.Literal["ac", "dc"]) -> _p:
        return self.get_basedir() / f"output_2_{ctype}.csv"

    def generate_merged_file(self, file_num: int):
        for ctype in ["ac", "dc"]:
            file_list = self.generate_file_list(file_num, ctype)
            df_list = read_file_list(file_list)
            merge_stage_2_files(df_list, self.get_merge_filepath(ctype))


def read_file_list(file_list: list[_p]) -> list[pd.DataFrame]:
    for file in file_list:
        assert file.exists(), f"文件不存在: {file}"

    return [pd.read_csv(file, encoding=encoding) for file in file_list]


def merge_stage_2_files(file_list: list[pd.DataFrame], output_path: _p) -> pd.DataFrame:
    """合并 stage-2 文件"""
    df = pd.concat(file_list)
    df.to_csv(output_path, index=False, encoding=encoding)
    return df
