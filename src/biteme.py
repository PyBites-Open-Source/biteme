from __future__ import annotations

import subprocess
import venv
from dataclasses import dataclass
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Optional, Protocol, Union
from zipfile import ZipFile

from more_itertools import only
import click
import requests


ENVIRONMENT_VARIABLE_PREFIX = "PYBITES"

DEFAULT_API_KEY = "free"
DEFAULT_REQUIREMENTS_URL = "https://raw.githubusercontent.com/pybites/platform-dependencies/master/requirements.txt"


StrPath = Union[str, PathLike[str]]


class HasEnvExe(Protocol):
    @property
    def env_exe(self) -> StrPath:
        ...


@dataclass(frozen=True)
class BiteMetadata:
    number: int
    title: str
    description: str
    level: str
    tags: list[str]
    free: bool
    score: int
    function: str


def download_bite_archive(bite_number: int, api_key: Optional[str] = None) -> ZipFile:
    # I'm choosing to have `api_key` be optional instead of setting it
    # to `DEFAULT_API_KEY` because I want to capture the edge-case where
    # someone passes the empty string, which will fail. Both `None` and
    # the empty string will evaluate as `False`, which means that
    # `api_key` will get the value of `DEFAULT_API_KEY`.
    api_key = api_key or DEFAULT_API_KEY
    url = f"http://codechalleng.es/api/bites/downloads/{api_key}/{bite_number}"
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


# Maybe this should be a class method?
def get_requirements(url: str = DEFAULT_REQUIREMENTS_URL) -> list[str]:
    with requests.get(url) as response:
        response.raise_for_status()
        return response.text.splitlines()  # type: ignore


class BiteEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context: HasEnvExe) -> None:
        python = context.env_exe
        requirements = get_requirements()
        subprocess.run([python, "-m", "pip", "install", *requirements], check=True)


def create_bite_venv(directory: StrPath) -> Path:
    venv_directory = Path(directory) / ".venv"
    builder = BiteEnvBuilder(clear=True, with_pip=True, upgrade_deps=True)
    builder.create(venv_directory)
    return venv_directory


def get_bite_metadata(bite_number: int) -> BiteMetadata:
    url = f"http://codechalleng.es/api/bites/{bite_number}"
    with requests.get(url) as response:
        response.raise_for_status()
        return BiteMetadata(**only(response.json()))


@click.command(context_settings={"auto_envvar_prefix": ENVIRONMENT_VARIABLE_PREFIX})
@click.version_option()
@click.argument("bite-number", type=click.IntRange(min=1, max=None))
@click.option(
    "-r",
    "--repository",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    help="The path to your local PyBites repository.",
    show_default=True,
)
@click.option(
    "-k",
    "--api-key",
    default=DEFAULT_API_KEY,
    help="Your PyBites API key.",
    show_default=True,
)
def cli(bite_number: int, api_key: str, repository: StrPath) -> None:
    bite_directory = download_and_extract_bite(bite_number, repository, api_key)
    create_bite_venv(bite_directory)
