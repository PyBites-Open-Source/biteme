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
    bite_dir = bites.download(api_key, bite_number, directory)
    typer.echo(bite_dir)


@cli.command()
def info(bite_number: int = typer.Argument(...)) -> None:
    """Get information about a codechallenge.es bite."""
    bite = bites.get_info(bite_number)
    typer.echo(bite)
