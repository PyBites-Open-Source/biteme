from __future__ import annotations

import argparse
import os
import subprocess
import venv
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from typing import NewType, Union
from zipfile import ZipFile

import requests

BiteNumber = NewType("BiteNumber", int)
StrPath = Union[str, os.PathLike[str]]


API_KEY = os.getenv("PYBITES_API_KEY", "free")


def download_zipped_bite(bite_number: BiteNumber) -> ZipFile:
    url = f"http://codechalleng.es/api/bites/downloads/{API_KEY}/{bite_number}"
    response = requests.get(url)
    return ZipFile(BytesIO(response.content))


def download_and_extract(bite_number: BiteNumber, directory: StrPath) -> Path:
    bite_directory = Path(directory) / f"{bite_number}"
    with download_zipped_bite(bite_number) as zipped_bite:
        zipped_bite.extractall(bite_directory)
    return bite_directory


class _BiteEnvBuilder(venv.EnvBuilder):
    @staticmethod
    def post_setup(context: SimpleNamespace) -> None:
        python = context.env_exe
        subprocess.run([python, "-m", "pip", "install", "pytest"])


def create_virtual_environment(directory: StrPath) -> None:
    builder = _BiteEnvBuilder(clear=True, with_pip=True, upgrade_deps=True)
    builder.create(Path(directory) / ".venv")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bite-number", type=int, required=True)
    parser.add_argument("-d", "--directory", required=True)

    args = parser.parse_args()

    bite_directory = download_and_extract(args.bite_number, args.directory)
    create_virtual_environment(bite_directory)


if __name__ == "__main__":
    main()
