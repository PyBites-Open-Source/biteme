from __future__ import annotations

import dataclasses
import io
import os
import zipfile
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import click
import more_itertools
import requests

import urllib.parse

_BITE_API_URL = "https://codechalleng.es/api/bites/"


@dataclasses.dataclass(frozen=True)
class _BiteInfo:
    number: int
    title: str
    description: str
    level: str
    tags: Tuple[str, ...]
    free: bool
    score: int
    function: str


def _get_bite_info(bite_number: int) -> _BiteInfo:
    url = urllib.parse.urljoin(_BITE_API_URL, f"{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    data = more_itertools.one(cast(List[Dict[str, Any]], response.json()))
    return _BiteInfo(
        number=data["number"],
        title=data["title"],
        description=data["description"],
        level=data["level"],
        tags=tuple(data["tags"]),
        free=data["free"],
        score=data["score"],
        function=data["function"],
    )


def _download_bite(
    bite_number: int, api_key: str, directory: Union[str, "os.PathLike[str]"]
) -> None:
    url = urllib.parse.urljoin(_BITE_API_URL, f"downloads/{api_key}/{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(directory)


_PositiveInt = click.IntRange(min=1)
_DirectoryPath = click.Path(file_okay=False, resolve_path=True)


def _directory_callback(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> str:
    if not value:
        bite_number: int = ctx.params["bite_number"]
        return f"bite{bite_number:04d}"
    return value


@click.group()
def cli() -> None:
    ...


@cli.command()
@click.argument("bite_number", type=_PositiveInt)
@click.option(
    "--api-key",
    default="free",
    show_default=True,
    envvar="PYBITES_API_KEY",
    show_envvar=True,
)
@click.argument(
    "directory",
    required=False,
    type=_DirectoryPath,
    callback=_directory_callback,
)
def download(
    bite_number: int, api_key: str, directory: Union[str, "os.PathLike[str]"]
) -> None:
    _download_bite(bite_number, api_key, directory)


@cli.command()
@click.argument("bite_number", type=_PositiveInt)
def info(bite_number: int) -> None:
    ...
