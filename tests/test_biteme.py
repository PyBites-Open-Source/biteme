from __future__ import annotations


import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture

import biteme


FREE_BITES = 1, 2, 3, 5, 30, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 238, 241


def test_download_zipped_bite(mocker: MockerFixture) -> None:
    spy = mocker.spy(requests, "get")
    zipped_bite = biteme.download_zipped_bite(bite=1, api_key="testing")
    spy.assert_called_once_with("http://codechalleng.es/api/bites/downloads/testing/1")
    assert set(zipped_bite.namelist()) == {
        "README.md",
        "bite.html",
        "summing.py",
        "test_summing.py",
    }


def test_main_succeeds(tmp_path: Path) -> None:
    runner = click.testing.CliRunner()
    result = runner.invoke(biteme.main, f"--bite 1 --output {tmp_path}")


#     assert result.exit_code == 0


# # def test_create_virtual_environment(tmp_path: Path) -> None:
# #     biteme.create_virtual_environment(tmp_path)
# #     assert (tmp_path / ".venv").is_dir()
