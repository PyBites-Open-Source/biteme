import pathlib
from typing import Generator

import _pytest.monkeypatch
import pytest
import typer.testing


CLIRunner = typer.testing.CliRunner


@pytest.fixture
def cli(
    tmp_path: pathlib.Path, monkeypatch: _pytest.monkeypatch.MonkeyPatch
) -> typer.testing.CliRunner:
    monkeypatch.chdir(tmp_path)
    return typer.testing.CliRunner()
