# %%
from __future__ import annotations

from io import BytesIO
from os import PathLike
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union
from zipfile import ZipFile

import requests


StrPath = Union[str, "PathLike[str]"]


def _extract_python_files(
    bite_archive: Union[StrPath, BytesIO, ZipFile], target_directory: StrPath
) -> Path:
    if not isinstance(bite_archive, ZipFile):
        bite_archive = ZipFile(bite_archive)

    target_directory = Path(target_directory)

    # XXX (Will): Should this be more precise? I want exactly two .py
    # files: "<module-name>.py" and "test_<module-name>.py", for some
    # string "<module-name>". I also know that if the zip archive was
    # made on macOS, I'll have a one-to-one correspondance between the
    # actual archive members found in "<archive-name>/" and the archive
    # members found in "__MACOSX/.<archive-name>/".
    python_module_names = [
        name
        for name in bite_archive.namelist()
        if not name.startswith("__MACOSX/") and name.endswith(".py")
    ]
    if len(python_module_names) != 2:
        # TODO (Will): Write a more helpful error message.
        raise RuntimeError("unrecognized bite archive")

    bite_archive.extractall(target_directory, members=python_module_names)

    for path in (target_directory / name for name in python_module_names):
        path.rename(target_directory / path.name)

    for subdirectory in filter(Path.is_dir, target_directory.iterdir()):
        subdirectory.rmdir()

    return directory


if __name__ == "__main__":
    url = "https://bite-zipfiles.s3.eu-west-3.amazonaws.com/pybites_bite1.zip"
    response = requests.get(url)
    archive = BytesIO(response.content)
    with TemporaryDirectory() as directory:
        directory = Path(directory)
        _extract_python_files(archive, directory)
        assert len(list(directory.iterdir())) == 2
