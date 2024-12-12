from pathlib import Path

import pandas as pd

from cathodic_collect.fileutils import get_output_file_encode

encoding = get_output_file_encode()


class DFReader(object):
    def read_csv(self, filename: Path) -> pd.DataFrame:
        assert filename.exists(), f"file {filename} not found"
        return pd.read_csv(filename, encoding=encoding)
