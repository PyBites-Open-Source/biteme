from __future__ import annotations

from typing import Optional

import click

from biteme import download_and_extract_bite


@click.group(context_settings={"auto_envvar_prefix": "PYBITES"})
@click.version_option()
def cli() -> None:
    ...


@cli.command()
@click.option("--api-key", default="free", show_default=True, show_envvar=True)
@click.argument("bite", required=True, type=click.IntRange(min=1))
@click.argument(
    "directory", required=False, type=click.Path(file_okay=False, writable=True)
)
def download(api_key: str, bite: int, directory: Optional[str] = None) -> None:
    download_and_extract_bite(api_key, bite, directory)


if __name__ == "__main__":
    cli()
