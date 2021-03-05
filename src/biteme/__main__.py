from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from biteme import bites


__all__ = ["cli"]


cli = typer.Typer(context_settings={"auto_envvar_prefix": "PYBITES"})


@cli.command()
def info(bite: int) -> None:
    bite_info = bites._info(bite)
    typer.echo(f"{bite_info=}")


@cli.command()
def download(
    bite: int = typer.Argument(...),
    directory: Optional[Path] = typer.Argument(
        None,
        writable=True,
        file_okay=False,
    ),
    api_key: Optional[str] = typer.Option(None),
) -> None:
    bites.download(bite, directory, api_key)


if __name__ == "__main__":
    cli()
