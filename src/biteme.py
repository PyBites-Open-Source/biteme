from __future__ import annotations

import io
import os
import shutil
import venv
from itertools import filterfalse
from pathlib import Path
from typing import BinaryIO, NewType, Union, cast
from urllib.parse import urljoin
from zipfile import ZipFile, ZipInfo

import requests

_BiteID = NewType("_BiteID", int)

_StrPath = Union[str, "os.PathLike[str]"]


def _download_archive(bite_id: _BiteID) -> ZipFile:
    filename = f"pybites_bite{bite_id}.zip"
    url = urljoin("https://bite-zipfiles.s3.eu-west-3.amazonaws.com", filename)
    response = requests.get(url)
    buffer = io.BytesIO(response.content)
    archive = ZipFile(buffer)
    archive.filename = filename
    return archive


def _is_macos_resource_fork(member: Union[str, ZipInfo]) -> bool:
    filename = member.filename if isinstance(member, ZipInfo) else member
    return filename.startswith("__MACOSX/")


def _find_python_module(directory: _StrPath) -> Path:
    for path in Path(directory).iterdir():
        if not path.name.startswith("test_") and path.suffix == ".py":
            return path
    raise ValueError(f"Cannot find a non-test python module in {directory}")


def _check_bite(directory: _StrPath) -> None:
    directory = Path(directory)
    python_module_name = _find_python_module(directory).name
    python_test_module_name = f"test_{python_module_name}"
    expected_filenames = {
        "bite.html",
        "README.md",
        python_module_name,
        python_test_module_name,
        "git.txt",
    }
    filenames = {path.name for path in directory.iterdir()}
    if filenames != expected_filenames:
        raise ValueError("Unrecognized bite archive")


def extract_bite(
    archive: Union[ZipFile, _StrPath, BinaryIO], directory: _StrPath
) -> Path:
    if not isinstance(archive, ZipFile):
        archive = ZipFile(archive)

    directory = Path(directory)
    directory.mkdir()

    for member in filterfalse(
        lambda member: member.is_dir() or _is_macos_resource_fork(member),
        archive.infolist(),
    ):
        destination = directory / os.path.basename(member.filename)
        with archive.open(member) as member_file, destination.open("xb") as output_file:
            shutil.copyfileobj(
                member_file,
                cast(BinaryIO, output_file),
                length=member.file_size,
            )

    _check_bite(directory)
    return directory


def _create_virtualenv(directory: _StrPath, bite_id: _BiteID) -> None:
    venv.create(
        Path(directory) / ".venv",
        with_pip=True,
        prompt=f"bite-{bite_id}",
        upgrade_deps=True,
    )


if __name__ == "__main__":
    bite_id = _BiteID(1)
    directory = Path(__file__).parents[1] / f"bites/{bite_id}"

    archive = _download_archive(bite_id)
    extract_bite(archive, directory)
    _create_virtualenv(directory, bite_id)
