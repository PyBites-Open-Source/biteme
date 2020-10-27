from __future__ import annotations

import subprocess
import venv
from io import BytesIO
from os import PathLike
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Union
from zipfile import ZipFile

import click
import requests


StrPath = Union[str, PathLike[str]]


def get_bite_directory(directory: StrPath, bite: int) -> Path:
    return Path(directory) / f"{bite}"


def download_zipped_bite(bite: int, api_key: str) -> ZipFile:
    url = f"http://codechalleng.es/api/bites/downloads/{api_key}/{bite}"
    with requests.get(url) as response:
        response.raise_for_status()
        return ZipFile(BytesIO(response.content))


def download_and_extract(bite: int, api_key: str, directory: StrPath) -> Path:
    bite_directory = get_bite_directory(directory, bite)
    with download_zipped_bite(bite, api_key) as zipped_bite:
        zipped_bite.extractall(bite_directory)
    return bite_directory


# class _EnvBuilder(venv.EnvBuilder):
#     def post_setup(self, context: SimpleNamespace) -> None:
#         python: str = context.env_exe
#         subprocess.run([python, "-m", "pip", "install", "pytest"])


# def create_virtual_environment(directory: StrPath) -> None:
#     builder = _EnvBuilder(clear=True, with_pip=True, upgrade_deps=True)
#     builder.create(directory)


@click.command()
@click.version_option()
@click.argument("bite", type=click.INT)
@click.option(
    "-k",
    "--api-key",
    default="free",
    envvar="PYBITES_API_KEY",
    help="Your PyBites API key.",
)
@click.option(
    "-r",
    "--repository",
    envvar="PYBITES_REPOSITORY",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    help="The directory to download the bite to.",
)
def main(bite: int, api_key: str, repository: StrPath) -> None:
    bite_directory = download_and_extract(bite, api_key, repository)
    venv.create(bite_directory / ".venv", with_pip=True, upgrade_deps=True)
