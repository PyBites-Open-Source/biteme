from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple
from urllib.parse import urljoin
from zipfile import ZipFile

import requests
from more_itertools import one


if TYPE_CHECKING:
    from _typeshed import StrPath


__all__ = ["download"]

_DEFAULT_API_KEY = "free"


_API_URL = "https://codechalleng.es/api/"
_INFO_URL = urljoin(_API_URL, "bites/")
_DOWNLOAD_URL = urljoin(_API_URL, "bites/downloads/")


def _download_archive(bite_number: int, api_key: Optional[str] = None) -> ZipFile:
    url = urljoin(_DOWNLOAD_URL, f"{api_key or _DEFAULT_API_KEY}/{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    return ZipFile(BytesIO(response.content))


def download(
    bite_number: int,
    directory: Optional["StrPath"] = None,
    api_key: Optional[str] = None,
) -> Path:
    """Download a bite.

    Args:
        bite_number: Bite number.
        directory (optional): Directory to extract the bite into.
            If not specified, the current working directory is used.
        api_key (optional): PyBites API key.

    Returns:
        A path to a directory with the bite content files.
    """
    bite_dir = Path(directory or Path.cwd()) / f"Bite {bite_number}"
    with _download_archive(bite_number, api_key) as archive:
        archive.extractall(bite_dir)
    return bite_dir


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
    url = urljoin(_INFO_URL, f"{bite_number}")
    response = requests.get(url)
    response.raise_for_status()
    data = one(response.json())
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
