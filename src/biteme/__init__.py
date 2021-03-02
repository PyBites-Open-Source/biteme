from __future__ import annotations

import dataclasses
import io
import os
import pathlib
import urllib.parse
import zipfile
from typing import Any, Dict, Optional, Tuple, Union, cast

import click
import more_itertools
import requests


_API_URL = "https://codechalleng.es/api/"
_BITES_URL = urllib.parse.urljoin(_API_URL, "bites/")
_DOWNLOAD_URL = urllib.parse.urljoin(_BITES_URL, "downloads/")


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
    url = urllib.parse.urljoin(_BITES_URL, f"{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    data = cast(Dict[str, Any], more_itertools.one(response.json()))
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


def _download_bite_archive(api_key: str, bite_number: int) -> zipfile.ZipFile:
    url = urllib.parse.urljoin(_DOWNLOAD_URL, f"{api_key}/{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    return zipfile.ZipFile(io.BytesIO(response.content))


def _download_and_extract_bite(
    api_key: str, bite_number: int, path: Optional[Union[str, "os.PathLike"]] = None
) -> None:
    path = pathlib.Path(path or os.getcwd())
    bite_dir = path / f"bite{bite_number:04d}"
    with _download_bite_archive(api_key, bite_number) as bite_archive:
        bite_archive.extractall(bite_dir)


@click.group(context_settings={"auto_envvar_prefix": "PYBITES"})
@click.version_option()
def cli() -> None:
    ...


@cli.command()
@click.option("--api-key", default="free", show_default=True, show_envvar=True)
@click.argument("bite", required=True, type=click.IntRange(min=1))
@click.argument(
    "directory", required=False, type=click.Path(file_okay=False, writable=True)
)
def download(api_key: str, bite: int, directory: Optional[str] = None) -> None:
    _download_and_extract_bite(api_key, bite, directory)
