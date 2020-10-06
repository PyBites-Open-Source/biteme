import zipfile
import pytest
from pathlib import Path


@pytest.fixture
def zipped_bite() -> zipfile.Path:
    return zipfile.Path(Path(__file__).parent / "pybites_bite1.zip")


def test_zipped_bite(zipped_bite: zipfile.Path) -> None:
    assert zipped_bite.is_dir()
    assert len(list(zipped_bite.iterdir())) == 5
