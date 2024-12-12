from pathlib import Path

import pytest


@pytest.fixture
def sample_base_dir(resource_folder: Path):
    return resource_folder / "2024-12-11-test"
