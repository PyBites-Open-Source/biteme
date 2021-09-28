from __future__ import annotations

import cgi
import io
import operator
import os
import pathlib
import zipfile
from typing import Union

import pydantic
import requests
import typer


class BiteInfo(pydantic.BaseModel):
    """Information about a codechalleng.es bite exercise."""

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
    """Get info for all the bites, sorted by number.

    Example:
        >>> bites = get_all_bite_info()

    """
    url = "https://codechalleng.es/api/bites/"
    response = requests.get(url)
    response.raise_for_status()
    bites = (BiteInfo(**data) for data in response.json())
    return sorted(bites, key=operator.attrgetter("number"))


def download_bite(
    api_key: str, number: int, directory: Union[str, os.PathLike[str]]
) -> pathlib.Path:
    url = f"https://codechalleng.es/api/bites/downloads/{api_key}/{number}"
    response = requests.get(url)
    response.raise_for_status()

    content_disposition = response.headers["content-disposition"]
    _, params = cgi.parse_header(content_disposition)
    filename = params["filename"]

    directory = pathlib.Path(directory).resolve()
    extract_dir = (directory / filename).with_suffix("")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
        zip.extractall(extract_dir)

    return extract_dir


cli = typer.Typer()


@cli.command()
def download(
    api_key: str = typer.Option("freebie", envvar="BITEME_API_KEY"),
    bite_number: int = typer.Argument(...),
    directory: pathlib.Path = typer.Option(".", file_okay=False),
) -> None:
    bite_dir = download_bite(api_key, bite_number, directory)
    typer.echo(bite_dir)


@cli.command()
def info(bite_number: int = typer.Argument(...)) -> None:
    bite = get_bite_info(bite_number)
    typer.echo(bite.json())
