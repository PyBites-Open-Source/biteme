from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from typer.testing import CliRunner as CLIRunner

import biteme


@pytest.fixture
def cli(tmp_path: Path, monkeypatch: MonkeyPatch) -> CLIRunner:
    monkeypatch.chdir(tmp_path)
    return CLIRunner()


@pytest.mark.parametrize(
    ("bite_number", "module_name"),
    [
        (1, "summing"),
        (101, "driving"),
    ],
)
def test_download(bite_number: int, module_name: str, cli: CLIRunner):
    result = cli.invoke(biteme.cli, ["download", f"{bite_number}"])
    assert result.exit_code == 0

    bite_dir = Path.cwd() / f"Bite {bite_number}"
    assert bite_dir.is_dir()
    assert {file.name for file in bite_dir.iterdir()} == {
        "README.md",
        "bite.html",
        f"{module_name}.py",
        f"test_{module_name}.py",
    }
