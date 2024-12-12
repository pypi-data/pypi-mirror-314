from __future__ import annotations

import pathlib as pl

import pandas as pd


class DFclass(object):
    """typed DataFrame. 这样的定义更加直观，方便日后维护。"""

    header: list[str]
    min_length: int

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.check()

    def check(self):
        assert len(self.header) != 0, "You should assign headers."

        if not (set(self.header) <= set(self.df.keys())):
            raise ValueError(
                "header is not correct.\n"
                + "\n".join(self.header)
                + "\n"
                + "---\n"
                + "\n".join(self.df.keys())
            )

        if len(self.df) < self.min_length:
            raise ValueError(f"data length is less than {self.min_length}.")

    @classmethod
    def set_df(cls, df: pd.DataFrame):
        return cls(df=df)

    def get_cols(self, names: list[str]) -> pd.DataFrame:
        if not set(names) <= set(self.header):
            raise ValueError(f"column {names} not found. You should add it to header")
        return self.df[names]

    def get_col(self, name: str) -> list:
        if name not in self.header:
            raise ValueError(f"column {name} not found. You should add it to header")
        return list(self.df[name])
