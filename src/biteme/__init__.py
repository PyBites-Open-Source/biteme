from __future__ import annotations

from typing import Any, Dict, List, Tuple, cast
from urllib.parse import urljoin

import requests
from more_itertools import one


_API_URL = "https://codechalleng.es/api/bites/"


import dataclasses


@dataclasses.dataclass(frozen=True)
class _BiteMetadata:
    number: int
    title: str
    description: str
    level: str
    tags: Tuple[str, ...]
    free: bool
    score: int
    function: str


def get_bite_metadata(bite: str) -> _BiteMetadata:
    with requests.get(f"https://codechalleng.es/api/bites/{bite}") as response:
        metadata: Dict[str, Any] = one(response.json())

    return _BiteMetadata(
        number=metadata["number"],
        title=metadata["title"],
        description=metadata["description"],
        level=metadata["level"],
        tags=tuple(metadata["tags"]),
        free=metadata["free"],
        score=metadata["score"],
        function=metadata["function"],
    )


def download_bite(bite: str):
    ...


# _StrPath = Union[str, "os.PathLike[str]"]

# /downloads/{api_key}/{bite}"
# _DEFAULT_REQUIREMENTS_URL = "https://raw.githubusercontent.com/pybites/platform-dependencies/master/requirements.txt"


# def download_bite_archive(
#     bite_number: int, api_key: Optional[str] = None
# ) -> zipfile.ZipFile:
#     api_key = api_key or _DEFAULT_API_KEY
#     url = _API_URL + f"/downloads/{api_key}/{bite_number}"
#     with requests.get(url) as response:
#         response.raise_for_status()
#         return zipfile.ZipFile(io.BytesIO(response.content))


# def download_and_extract_bite(
#     bite_number: int, directory: _StrPath, api_key: Optional[str] = None
# ) -> pathlib.Path:
#     bite_directory = pathlib.Path(directory) / f"{bite_number}"
#     with download_bite_archive(bite_number, api_key) as archive:
#         archive.extractall(bite_directory)
#     return bite_directory


# def get_requirements(url: str = _DEFAULT_REQUIREMENTS_URL) -> List[str]:
#     with requests.get(url) as response:
#         response.raise_for_status()
#         return response.text.splitlines()


# @click.command(
#     context_settings={
#         "help_option_names": ["-h", "--help"],
#         "auto_envvar_prefix": "PYBITES",
#     }
# )
# @click.version_option()
# @click.argument("bite")
# @click.option(
#     "-r",
#     "--repository",
#     required=True,
#     type=click.Path(file_okay=False, writable=True),
#     help="The path to your local PyBites repository.",
# )
# @click.option("-k", "--api-key", help="PyBites API key")
# def cli(bite_number: int, api_key: str, repository: _StrPath) -> None:
#     ...
#     # HACK: Raise a `RuntimeError` if the bite's environment is not the
#     # default one. Not worth making a custom exception for now. I just
#     # want some sort of error thrown so that you don't have a faulty environment.
#     # bite_metadata = get_bite_metadata(bite_number)
#     # if bite_metadata.function != "default":
#     #     raise RuntimeError(f"unsupported bite {bite_number}")

#     # bite_directory = download_and_extract_bite(bite_number, repository, api_key)
#     # create_bite_venv(bite_directory)
