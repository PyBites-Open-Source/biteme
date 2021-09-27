from __future__ import annotations

import cgi
import io
import operator
import os
import pathlib
import zipfile
from typing import Any
from typing import Union

import pydantic
import requests
import typer


class BiteInfo(pydantic.BaseModel):
    class Config:
        allow_mutation = False

    number: int
    title: str
    description: str
    level: str
    tags: frozenset[str]
    free: bool
    score: int
    function: str


def get_bite_info(number: int) -> BiteInfo:
    """Get info for a specific bite.

    Example:
        >>> bite = get_bite_info(1)

    """
    url = f"https://codechalleng.es/api/bites/{number}"
    response = requests.get(url)
    response.raise_for_status()
    [data] = response.json()
    return BiteInfo(**data)


def get_all_bite_info() -> list[BiteInfo]:
    """Get info for all the bites.

    Example:
        >>> bites = get_all_bite_info()

    """
    url = "https://codechalleng.es/api/bites/"
    response = requests.get(url)
    response.raise_for_status()
    return [BiteInfo(**data) for data in response.json()]


def download_bite(
    api_key: str, number: int, directory: Union[str, os.PathLike[str]]
) -> pathlib.Path:
    url = f"https://codechalleng.es/api/bites/downloads/{api_key}/{number}"
    response = requests.get(url)
    response.raise_for_status

    content_disposition = response.headers["content-disposition"]
    _, header_options = cgi.parse_header(content_disposition)
    filename = header_options["filename"]

    directory = pathlib.Path(directory).resolve()
    extract_dir = (directory / filename).with_suffix("")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
        zip.extractall(extract_dir)

    return extract_dir


cli = typer.Typer()


@cli.command()
def download(
    *,
    api_key: str = typer.Option(..., envvar="BITEME_API_KEY"),
    number: int = typer.Argument(..., metavar="BITE_NUMBER"),
    directory: pathlib.Path = typer.Option(".", file_okay=False, resolve_path=True),
) -> None:
    ...
