import glob
import os
import sys
import pathlib
from typing import Callable, Union

import pytest
from click.testing import CliRunner as CLIRunner
import more_itertools

import biteme


if sys.version_info >= (3, 9):
    removeprefix = str.removeprefix
else:

    def removeprefix(string: str, prefix: str) -> str:
        if string.startswith(prefix):
            return string[len(prefix) :]
        return string[:]


def _assert_is_valid_bite_directory(path: Union[str, "os.PathLike[str]"]):
    __tracebackhide__ = True

    path = pathlib.Path(path)
    assert path.is_dir()

    test_file = more_itertools.one(path.glob("test_*.py"))
    try:
        test_file = more_itertools.one(path.glob("test_*.py"))
    except ValueError:
        raise AssertionError

    test_filename = test_file.name
    py_filename = removeprefix(test_filename, "test_")

    filenames = {child.name for child in path.iterdir()}
    expected = {"README.md", "bite.html", py_filename, test_filename}

    assert filenames == expected


@pytest.fixture
def bite_number() -> int:
    return 1


@pytest.fixture
def directory(bite_number: int) -> pathlib.Path:
    return pathlib.Path(f"bite{bite_number:04d}")


def test_download(
    bite_number: int, directory: pathlib.Path, cli_runner: CLIRunner
) -> None:
    result = cli_runner.invoke(
        biteme.cli, ["download", f"{bite_number}", f"{directory}"]
    )
    assert result.exit_code == 0
    _assert_is_valid_bite_directory(directory)
