from typing import Generator, Iterator
import click.testing
import pytest


@pytest.fixture(scope="function")
def cli_runner() -> Generator[click.testing.CliRunner, None, None]:
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem() as cwd:
        yield runner
