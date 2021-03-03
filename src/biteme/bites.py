from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple
from urllib.parse import urljoin
from zipfile import ZipFile

import more_itertools
import requests


if TYPE_CHECKING:

    from _typeshed import StrPath


__all__ = ["download"]


_API_URL = "https://codechalleng.es/api/"


@dataclass(frozen=True)
class _Info:
    number: int
    title: str
    description: str
    level: str
    tags: Tuple[str, ...]
    free: bool
    score: int
    function: str


def _info(bite_number: int) -> _Info:
    url = urljoin(_API_URL, f"bites/{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    data = more_itertools.one(response.json())
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


def _download_archive(api_key: str, bite_number: int) -> ZipFile:
    url = urljoin(_API_URL, f"bites/downloads/{api_key}/{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    return ZipFile(io.BytesIO(response.content))


def download(
    api_key: str, bite_number: int, directory: Optional["StrPath"] = None
) -> Path:
    """Download a bite.

    Args:
        api_key: PyBites API key.
        bite_number: Bite number.
        directory (optional): Directory to extract the bite into.
            If not specified, the current working directory is used.

    Returns:
        The bite directory.
    """
    directory = Path(directory) if directory else Path.cwd()
    bite_dir = directory / f"Bite {bite_number}"
    with _download_archive(api_key, bite_number) as archive:
        archive.extractall(bite_dir)
    return bite_dir
