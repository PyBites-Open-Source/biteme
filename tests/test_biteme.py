from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest
from _pytest.fixtures import SubRequest

import biteme


FIXTURES_DIRECTORY = Path(__file__).parent / "fixtures"


@pytest.fixture(params=["archive.zip"], ids=str)
def zipped_bite(request: SubRequest) -> ZipFile:
    filename = request.param
    return ZipFile(FIXTURES_DIRECTORY / filename)


def test_create_virtual_environment(tmp_path: Path) -> None:
    biteme.create_virtual_environment(tmp_path)
    assert (tmp_path / ".venv").is_dir()
