from __future__ import annotations

import subprocess
from subprocess import run
import venv
from dataclasses import dataclass
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import List, Optional, Protocol, Union, runtime_checkable
from zipfile import ZipFile

import click
import requests
from more_itertools import one
from typing_extensions import runtime


ENVIRONMENT_VARIABLE_PREFIX = "PYBITES"

DEFAULT_API_KEY = "free"

API_URL = "https://codechalleng.es/api/bites"
DEFAULT_REQUIREMENTS_URL = "https://raw.githubusercontent.com/pybites/platform-dependencies/master/requirements.txt"


StrPath = Union[str, PathLike[str]]


@dataclass(frozen=True)
class BiteMetadata:
    number: int
    title: str
    description: str
    level: str
    tags: List[str]
    free: bool
    score: int
    function: str


def get_bite_metadata(bite_number: int) -> BiteMetadata:
    url = API_URL + f"/{bite_number}"
    with requests.get(url) as response:
        response.raise_for_status()
        return BiteMetadata(**one(response.json()))


def download_bite_archive(bite_number: int, api_key: Optional[str] = None) -> ZipFile:
    api_key = api_key or DEFAULT_API_KEY
    url = API_URL + f"/downloads/{api_key}/{bite_number}"
    with requests.get(url) as response:
        response.raise_for_status()
        return ZipFile(BytesIO(response.content))


def download_and_extract_bite(
    bite_number: int, directory: StrPath, api_key: Optional[str] = None
) -> Path:
    bite_directory = Path(directory) / f"{bite_number}"
    with download_bite_archive(bite_number, api_key) as archive:
        archive.extractall(bite_directory)
    return bite_directory


def get_requirements(url: str = DEFAULT_REQUIREMENTS_URL) -> List[str]:
    with requests.get(url) as response:
        response.raise_for_status()
        return response.text.splitlines()


@runtime_checkable
class _HasEnvExe(Protocol):
    @property
    def env_exe(self) -> StrPath:
        ...


class BiteEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context: object) -> None:
        assert isinstance(context, _HasEnvExe)
        python = context.env_exe
        requirements = get_requirements()
        subprocess.run([python, "-m", "pip", "install", *requirements], check=True)


def create_bite_venv(directory: StrPath) -> Path:
    venv_directory = Path(directory) / ".venv"
    venv.create(venv_directory, clear=True, with_pip=True, upgrade_deps=True)
    return venv_directory


@click.command(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "auto_envvar_prefix": ENVIRONMENT_VARIABLE_PREFIX,
    }
)
@click.version_option()
@click.argument(
    "bite-number",
    type=click.IntRange(min=1, max=None),
    metavar="BITE",
)
@click.option(
    "-r",
    "--repository",
    required=True,
    type=click.Path(file_okay=False, writable=True),
    help="The path to your local PyBites repository.",
)
@click.option(
    "-k",
    "--api-key",
    default=DEFAULT_API_KEY,
    show_default=True,
    help="The PyBites API key.",
)
def cli(bite_number: int, api_key: str, repository: StrPath) -> None:
    # HACK: Raise a `RuntimeError` if the bite's environment is not the
    # default one. Not worth making a custom exception for now. I just
    # want some sort of error thrown so that you don't have a faulty environment.
    bite_metadata = get_bite_metadata(bite_number)
    if bite_metadata.function != "default":
        raise RuntimeError(f"unsupported bite {bite_number}")

    bite_directory = download_and_extract_bite(bite_number, repository, api_key)
    create_bite_venv(bite_directory)
