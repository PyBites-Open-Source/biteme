from __future__ import annotations

import subprocess
import venv
from dataclasses import dataclass
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Literal, Protocol, Union, runtime_checkable
from zipfile import ZipFile

from more_itertools import first_true
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


def download_and_extract_bite(bite: int, api_key: str, directory: StrPath) -> Path:
    bite_directory = get_bite_directory(directory, bite)
    with download_zipped_bite(bite, api_key) as zipped_bite:
        zipped_bite.extractall(bite_directory)
    return bite_directory


def get_bite_requirements() -> list[str]:
    url = "https://raw.githubusercontent.com/pybites/platform-dependencies/master/requirements.txt"
    with requests.get(url) as response:
        response.raise_for_status()
        return response.text.split()  # type: ignore


class _HasEnvExe(Protocol):
    @property
    def env_exe(self) -> StrPath:
        ...


class _BiteEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context: _HasEnvExe) -> None:
        python = context.env_exe
        requirements = get_bite_requirements()
        subprocess.run(args=[python, "-m", "pip", "install", *requirements])


def create_virtual_environment(directory: StrPath) -> None:
    builder = _BiteEnvBuilder(clear=True, with_pip=True, upgrade_deps=True)
    builder.create(directory)


@dataclass(frozen=True)
class BiteMetadata:
    number: int
    title: str
    description: str
    level: str
    tags: list[str]
    score: int
    function: str


def get_bite_metadata(bite: int) -> BiteMetadata:
    url = "http://codechalleng.es/api/bites/"
    with requests.get(url) as response:
        response.raise_for_status()
        if metadata := first_true(
            (BiteMetadata(**kwargs) for kwargs in response.json()),
            pred=lambda metadata: metadata.number == bite,
        ):
            return metadata
        raise ValueError


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
    bite_directory = download_and_extract_bite(bite, api_key, repository)
    create_virtual_environment(bite_directory / ".venv")
