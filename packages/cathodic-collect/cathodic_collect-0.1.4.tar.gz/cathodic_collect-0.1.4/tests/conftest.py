from pathlib import Path

import pytest

from cathodic_collect.reader.dfreader import DFReader


@pytest.fixture
def resource_folder():
    return Path(__file__).parent.parent / "src/resources"


@pytest.fixture
def base_dir():
    return Path(__file__).parent.parent / "src/resources" / "2024-12-04-21-32-11b751a"


@pytest.fixture
def tmp_folder():
    return Path("./tmp")


@pytest.fixture
def df_reader():
    return DFReader()
