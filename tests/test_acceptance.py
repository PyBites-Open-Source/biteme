from pathlib import Path

import click.testing
import pytest
from _pytest.monkeypatch import MonkeyPatch

import biteme


@pytest.mark.parametrize(
    "number, module",
    [
        (1, "summing"),
        (101, "driving"),
    ],
)
def test_download(number: int, module: str, tmp_path: Path, monkeypatch: MonkeyPatch):
    monkeypatch.chdir(tmp_path)

    cli_runner = click.testing.CliRunner()
    result = cli_runner.invoke(biteme.cli, ["download", f"{number}"])
    assert result.exit_code == 0

    bite_dir = tmp_path / f"bite{number:04d}"
    assert {file.name for file in bite_dir.iterdir()} == {
        "README.md",
        "bite.html",
        f"{module}.py",
        f"test_{module}.py",
    }
