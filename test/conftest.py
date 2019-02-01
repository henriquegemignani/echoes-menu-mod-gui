import dataclasses
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def test_files_dir() -> Path:
    return Path(__file__).parent.joinpath("test_files")


class DataclassTestLib:
    def mock_dataclass(self, obj) -> MagicMock:
        return MagicMock(spec=[field.name for field in dataclasses.fields(obj)])


@pytest.fixture()
def dataclass_test_lib() -> DataclassTestLib:
    return DataclassTestLib()
