from __future__ import annotations

import venv
from io import BytesIO
from itertools import filterfalse
from os import PathLike
from pathlib import Path
from shutil import copyfileobj
from types import SimpleNamespace
from typing import BinaryIO, NewType, Union, cast
from urllib.parse import urljoin
from zipfile import ZipFile, ZipInfo

import requests
from more_itertools import first_true

BiteID = NewType("BiteID", int)


def download(bite_id: BiteID) -> ZipFile:
    """Download a zip archive containing a bite."""
    filename = f"pybites_bite{bite_id}.zip"
    url = urljoin("https://bite-zipfiles.s3.eu-west-3.amazonaws.com", filename)
    response = requests.get(url)
    buffer = BytesIO(response.content)
    archive = ZipFile(buffer)
    archive.filename = filename
    return archive


def _is_macos_resource_fork(member: ZipInfo) -> bool:
    return member.filename.startswith("__MACOSX/")


def extract(archive: ZipFile, directory: Union[str, PathLike[str]]) -> Path:
    directory = Path(directory)

    for member in filterfalse(
        lambda member: member.is_dir() or _is_macos_resource_fork(member),
        archive.infolist(),
    ):
        basename = Path(member.filename).name
        target = directory / basename
        copyfileobj(
            archive.open(member),
            cast(BinaryIO, target.open("xb")),
            length=member.file_size,
        )

    return directory


def _find_python_module(directory: Union[str, PathLike[str]]) -> Path:
    if python_module := first_true(
        Path(directory).iterdir(),
        pred=lambda path: path.match("*.py") and not path.match("test_*.py"),
    ):
        return python_module
    raise FileNotFoundError


def _validate_bite_directory(directory: Union[str, PathLike[str]]) -> None:
    directory = Path(directory)
    python_module_name = _find_python_module(directory).name
    expected_names = {
        "README.md",
        "bite.html",
        "git.txt",
        python_module_name,
        f"test_{python_module_name}",
    }
    if {path.name for path in directory.iterdir()} != expected_names:
        raise RuntimeError


class BiteEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context: SimpleNamespace) -> None:
        # TODO (Will): Install additional requirements like `pytest`.
        super().post_setup(context)


def create_venv(directory: Union[str, PathLike[str]], bite_id: BiteID) -> None:
    builder = BiteEnvBuilder(with_pip=True, prompt=f"bite-{bite_id}", upgrade_deps=True)
    # XXX (Will): Upgrading the dependencies is a subprocess call and it spits
    # it out to stdout. I tried redirecting stdout to stderr with
    # `contextlib.redirect_stdout` but that didn't work.
    builder.create(Path(directory) / ".venv")


def main(directory: Union[str, PathLike[str]], bite_id: BiteID) -> None:
    directory = Path(directory) / f"{bite_id}"
    directory.mkdir()

    archive = download(bite_id)
    extract(archive, directory)
    create_venv(directory, bite_id)
