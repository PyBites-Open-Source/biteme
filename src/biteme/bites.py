from __future__ import annotations

import dataclasses
import io
import os
import pathlib
import urllib.parse
import zipfile
from typing import Any, Dict, Optional, Tuple, Union, cast

import more_itertools
import requests


__all__ = ["download_and_extract"]


_API_URL = "https://codechalleng.es/api/"
_BITES_URL = urllib.parse.urljoin(_API_URL, "bites/")
_DOWNLOAD_URL = urllib.parse.urljoin(_BITES_URL, "downloads/")


@dataclasses.dataclass(frozen=True)
class _Info:
    number: int
    title: str
    description: str
    level: str
    tags: Tuple[str, ...]
    free: bool
    score: int
    function: str


def _get_info(number: int) -> _Info:
    url = urllib.parse.urljoin(_BITES_URL, f"{number}")
    response = requests.get(url)
    response.raise_for_status()
    data = cast(Dict[str, Any], more_itertools.one(response.json()))
    return _Info(
        number=data["number"],
        title=data["title"],
        description=data["description"],
        level=data["level"],
        tags=tuple(data["tags"]),
        free=data["free"],
        score=data["score"],
        function=data["function"],
    )


def _download_zip_file(api_key: str, number: int) -> zipfile.ZipFile:
    url = urllib.parse.urljoin(_DOWNLOAD_URL, f"{api_key}/{number}")
    response = requests.get(url)
    response.raise_for_status()
    return zipfile.ZipFile(io.BytesIO(response.content))


def download_and_extract(
    api_key: str,
    number: int,
    path: Optional[Union[str, "os.PathLike[str]"]] = None,
) -> None:
    """Download and extract a PyBites bite.

    Args:
        api_key: PyBites API key.
        bite_number: Number of the bite to download.
        path (optional): Path to extract the bite directory to.
            If not provided, the current working directory is used.
    """
    path = pathlib.Path(path or os.getcwd())
    bite_dir = path / f"bite{number:04d}"
    with _download_zip_file(api_key, number) as zip_file:
        zip_file.extractall(bite_dir)
