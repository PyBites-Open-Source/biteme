import os
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import pytest
from _pytest.fixtures import SubRequest

import biteme

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(params=["archive.zip", "macos-archive.zip"], ids=str)
def archive(request: SubRequest) -> ZipFile:
    archive_path = FIXTURE_DIR / str(request.param)
    return ZipFile(archive_path)


@pytest.fixture
def directory(tmpdir: Union[str, "os.PathLike[str]"]) -> Path:
    return Path(tmpdir)


def test_extract(archive: ZipFile, directory: Path) -> None:
    expected_filenames = {
        "bite.html",
        "README.md",
        "summing.py",
        "test_summing.py",
        "git.txt",
    }
    biteme.extract(archive, directory)
    actual_filenames = {str(path.name) for path in directory.iterdir()}
    assert actual_filenames == expected_filenames


@pytest.fixture
def bite_id() -> biteme.BiteID:
    return biteme.BiteID(1)


# XXX (Will): This test is slow.
def test_create_virtualenv(directory: Path, bite_id: biteme.BiteID) -> None:
    biteme.create_virtualenv(directory, bite_id)
    assert {path.name for path in directory.iterdir()} == {".venv"}
