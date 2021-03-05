from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from biteme import pybites


__all__ = ["cli"]


cli = typer.Typer(context_settings={"auto_envvar_prefix": "PYBITES"})


@cli.command()
def info(bite: int) -> None:
    bite_info = pybites._bite_info(bite)
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
    pybites.download_bite(bite, directory, api_key)


if __name__ == "__main__":
    cli()
