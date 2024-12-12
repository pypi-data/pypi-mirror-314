from pathlib import Path

import pytest


@pytest.fixture
def base_dir():
    return Path("./tmp/pics")


@pytest.fixture
def tmp_dir():
    return Path("./tmp/")
