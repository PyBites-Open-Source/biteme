from pathlib import Path

from typer.testing import CliRunner

from biteme.cli import cli

runner = CliRunner()


def test_cli_download():
    # TODO: provide default api token for free Bites
    result = runner.invoke(cli, ["download", "123", "101"])
    assert result.exit_code == 0
    download_dir = result.stdout.strip()
    assert download_dir.endswith("biteme/pybites_bite101")
    assert Path(download_dir).exists()


def test_cli_info():
    result = runner.invoke(cli, ["info", "101"])
    assert result.exit_code == 0
    assert "number=101" in result.stdout
    expected_title = "title='F-strings and a simple if/else'"
    assert expected_title in result.stdout
