import os
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import pytest
from _pytest.fixtures import SubRequest

import biteme

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(params=["archive.zip", "macos-archive.zip"])
def archive(request: SubRequest) -> ZipFile:
    archive_path = FIXTURE_DIR / str(request.param)
    return ZipFile(archive_path)


@pytest.fixture
def directory(tmpdir: Union[str, "os.PathLike[str]"]) -> Path:
    return Path(tmpdir)


def test_extract_bite(archive: ZipFile, directory: Path) -> None:
    biteme.extract_bite(archive, directory)
    assert len(list(directory.iterdir())) == 5
