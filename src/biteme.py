from __future__ import annotations

import io
import os
import shutil
from venv import EnvBuilder
from itertools import filterfalse
from pathlib import Path
from typing import BinaryIO, NewType, Union, cast
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
    filename = member.filename if isinstance(member, ZipInfo) else member
    return filename.startswith("__MACOSX/")


def extract_bite(
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
        destination = directory / os.path.basename(member.filename)
        with archive.open(member) as member_file, destination.open("xb") as output_file:
            shutil.copyfileobj(
                member_file,
                cast(BinaryIO, output_file),
                length=member.file_size,
            )

    return directory


def _create_virtualenv(directory: _StrPath) -> None:
    builder = EnvBuilder(with_pip=True, prompt=f"bite-{bite_id}")
    builder.create(directory)


if __name__ == "__main__":

    import tempfile

    bite_id = _BiteID(1)
    archive = _download(bite_id)

    with tempfile.TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory) / f"{bite_id}"
        directory.mkdir()

        extract_bite(archive, directory)

        for child in directory.iterdir():
            print(f"{child}")
