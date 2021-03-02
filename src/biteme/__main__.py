from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional

import click

from . import bites


if TYPE_CHECKING:
    from _typeshed import StrPath


__all__ = ["cli"]


_PositiveInt = click.IntRange(min=1)
_WritableDirectoryPath = click.Path(file_okay=False, writable=True)


@click.group(context_settings={"auto_envvar_prefix": "PYBITES"})
@click.version_option()
def cli() -> None:
    ...


@cli.command()
@click.option("--api-key", default="free", show_default=True, show_envvar=True)
@click.argument("bite", required=True, type=_PositiveInt)
@click.argument("directory", required=False, type=_WritableDirectoryPath)
def download(api_key: str, bite: int, directory: Optional["StrPath"]) -> None:
    bites.download(api_key, bite, directory)


if __name__ == "__main__":
    cli()
