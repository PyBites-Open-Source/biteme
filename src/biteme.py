from __future__ import annotations

import io
import os
import shutil
import tempfile
from contextlib import ExitStack
from itertools import filterfalse
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, BinaryIO, NewType, Union
from urllib.parse import urljoin
from zipfile import ZipFile, ZipInfo

import requests


_BiteID = NewType("_BiteID", int)

_StrPath = Union[str, "os.PathLike[str]"]


def _download(bite_id: _BiteID) -> ZipFile:
    filename = f"pybites_bite{bite_id}.zip"
    url = urljoin("https://bite-zipfiles.s3.eu-west-3.amazonaws.com", filename)
    response = requests.get(url)
    buffer = io.BytesIO(response.content)
    archive = ZipFile(buffer)
    archive.filename = filename
    return archive


def _is_macos_resource_fork(member: Union[str, ZipInfo]) -> bool:
    if isinstance(member, ZipInfo):
        member = member.filename
    return member.startswith("__MACOSX/")


def _extract(
    archive: Union[ZipFile, _StrPath, BinaryIO], directory: _StrPath
) -> Path:
    if not isinstance(archive, ZipFile):
        archive = ZipFile(archive)

    directory = Path(directory)

    # XXX (Will): Should this be more precise? I want exactly two .py
    # files: "<module-name>.py" and "test_<module-name>.py", for some
    # string "<module-name>". I also know that if the zip archive was
    # made on macOS, I'll have a one-to-one correspondance between the
    # actual archive members found in "<archive-name>/" and the archive
    # members found in "__MACOSX/.<archive-name>/".
    for member in filterfalse(
        lambda member: member.is_dir() or _is_macos_resource_fork(member),
        archive.infolist(),
    ):
        target_path = directory / os.path.basename(member.filename)
        with archive.open(member) as source, target_path.open("wb") as target:
            shutil.copyfileobj(source, target, member.file_size)

    return directory


if __name__ == "__main__":
    bite_id = _BiteID(1)
    archive = _download(bite_id)

    directory = Path(__file__).parents[1] / f"{bite_id}"
    directory.mkdir()

    _extract(archive, directory)

    for child in directory.iterdir():
        print(f"{child}")
