from pathlib import Path

import typer

from . import bites

__all__ = ["cli"]

cli = typer.Typer()


@cli.command()
def download(
    api_key: str = typer.Argument(...),
    bite_number: int = typer.Argument(...),
    directory: Path = typer.Argument(".", file_okay=False),
) -> None:
    """Download a codechalleng.es bite."""
    path = bites.download_bite(api_key, bite_number, directory)
    typer.echo(path)


@cli.command()
def info(bite_number: int = typer.Argument(...)) -> None:
    """Get information about a codechallenge.es bite."""
    info = bites.get_bite_info(bite_number)
    typer.echo(info)
