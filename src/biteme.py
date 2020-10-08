# %%
from __future__ import annotations

from io import BytesIO
from os import PathLike
from pathlib import Path
from tempfile import TemporaryDirectory, TemporaryFile
from typing import Iterator, NewType, Union
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

# response = requests.get(url)
# archive = ZipFile(BytesIO(response.content), mode="r")
# directory = TemporaryDirectory()

# new_archive = _clean_archive(archive)
# new_archive

#     if not _is_macos_zip_archive(archive):
#         return archive

#     member_names = archive.namelist()
#     if not len(archive.namelist()) == 2:
#         raise RuntimeError("Expected ")


# # with
# # zip_file2 = ZipFile("pybites_bite1.zip", mode="w")
# # for name in zip_file1.namelist():
# #     if not name.startswith("__MACOSX/"):

# #         zip_file2.writestr(name,

# # with (Path(__file__).parents[1] / "bite1.zip").open(mode="wb") as file:
# #     file.write(response.content)
# # # %%
# # with NamedTemporaryFile(mode="wb") as zip_file:
# #     zip_file.write(response.content)
# #     shutil.unpack_archive(zip_file.name, bites_dir, "zip")
# # print(list(bites_dir.iterdir()))

# # archive = ZipFile(BytesIO(response.content))
# # archive.extractall("/tmp")


# # def make_bite_directory(path: Union[str, os.PathLike], bite_id: BiteID) -> None:


# # # archive.extractall(
# # #     filter(
# # #         lambda name: not name.startswith("__MACOSX") and name.endswith(".py"),
# # #         archive.namelist(),
# # #     ),
# # # )
# # # if "__MACOSX" in archive.namelist():
# # #     ...
# # # else:
# # # ...

# # # archive.extractall(temporary_directory, members=["pybites_bite1/summing.py"])
# # # for directory, subdirectories, filenames in os.walk(temporary_directory):
# # #     print(f"{directory=}")
# # #     print(f"{subdirectories=}")
# # #     print(f"{filenames=}")


# # # %%


# # # root = zipfile.Path(archive)
# # # for child in root.iterdir():
# # #     print(f"{child.name=}")
# # # # root = root / "pybites_bite1"
# # # archive = ZipFile(root / "pybites_bite1")
# # # zip_root = zipfile.Path(zip_archive)
# # # print(zip_root)
# # # print(zip_root)

# # # %%
# # bite_dir = Path(__file__).parents[1] / "bites"

# # archive = ZipFile(BytesIO((bite_dir / "pybites_bite1.zip").read_bytes()))
# # root = zipfile.Path(archive)
# # for child in root.iterdir():
# #     print(f"{child.name=}")

# # # zip_archive = ZipFile(BytesIO(zip_file.read_bytes()))
# # # zip
# # # zip_root = zipfile.Path(zip_archive)
# # # print(list(zip_root.iterdir()))

# # # %%

# # %%

# %%
