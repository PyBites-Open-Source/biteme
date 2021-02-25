from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner
Î
import biteme


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    path = tmp_path / "pybites"
    path.mkdir()
    return path


@pytest.fixture
def bite_number() -> int:
    return 1




def test_cli(runner: CliRunner, repository: Path, bite_number: int) -> None:
    assert repository.is_dir()
    result = runner.invoke(biteme.cli, [f"--repository={repository}", f"{bite_number}"])
    # assert result.output


# error_message += "RecordType: {type} with ID: {id} has None for: {field}".format(
#     type=record.type, id=record.id, field=field
# )

# def test__get_bite_directory(tmp_path: Path) -> None:
#     directory = _get_bite_directory(tmp_path, 1)
#     assert directory == tmp_path / "1"


# def test__download_zipped_bite(mocker: MockerFixture) -> None:
#     spy = mocker.spy(requests, "get")
#     zipped_bite = biteme._download_zipped_bite(bite_number=1, api_key="testing")
#     spy.assert_called_once_with("http://codechalleng.es/api/bites/downloads/testing/1")
#     assert zipped_bite.namelist() == [
#         "README.md",
#         "bite.html",
#         "summing.py",
#         "test_summing.py",
#     ]


# def test__get_bite_requirements(mocker: MockerFixture) -> None:
#     spy = mocker.spy(requests, "get")
#     requirements = biteme._get_bite_requirements()
#     spy.assert_called_once_with(
#         "https://raw.githubusercontent.com/pybites/platform-dependencies/master/requirements.txt"
#     )
#     assert requirements == [
#         "attrs==19.3.0",
#         "beautifulsoup4==4.8.1",
#         "bs4==0.0.1",
#         "certifi==2020.4.5.1",
#         "cffi==1.14.0",
#         "chardet==3.0.4",
#         "click==7.1.2",
#         "coverage==5.1",
#         "cryptography==2.9.2",
#         "feedparser==5.2.1",
#         "Flask==1.1.2",
#         "gender-guesser==0.4.0",
#         "idna==2.9",
#         "itsdangerous==1.1.0",
#         "Jinja2==2.11.2",
#         "joblib==0.15.1",
#         "MarkupSafe==1.1.1",
#         "more-itertools==8.3.0",
#         "nltk==3.5",
#         "numpy==1.18.4",
#         "packaging==20.4",
#         "pandas==1.0.3",
#         "pluggy==0.13.1",
#         "py==1.8.1",
#         "pycparser==2.20",
#         "pyparsing==2.4.7",
#         "pytest==5.4.2",
#         "pytest-asyncio==0.12.0",
#         "pytest-cov==2.9.0",
#         "python-dateutil==2.8.1",
#         "pytz==2020.1",
#         "regex==2020.5.14",
#         "requests==2.23.0",
#         "six==1.15.0",
#         "soupsieve==2.0.1",
#         "textblob==0.15.3",
#         "tqdm==4.46.0",
#         "urllib3==1.25.9",
#         "wcwidth==0.1.9",
#         "Werkzeug==1.0.1",
#         "xlrd==1.2.0",
#     ]


# def test_create_virtual_environment(tmp_path: Path) -> None:
#     biteme.create_virtual_environment(tmp_path)
