import cgi
import io
import zipfile
import os
from pathlib import Path
from typing import FrozenSet
from typing import Union

import pydantic
import requests


class BiteInfo(pydantic.BaseModel):
    """Information about a codechalleng.es bite exercise."""

    class Config:
        allow_mutation = False

    number: int
    title: str
    description: str
    level: str
    tags: FrozenSet[str]
    free: bool
    score: int
    function: str


def info(bite_number: int) -> BiteInfo:
    """Get info for a codechalleng.es bite exercise."""
    url = f"https://codechalleng.es/api/bites/{bite_number}"
    response = requests.get(url)
    response.raise_for_status()
    [data] = response.json()
    return BiteInfo(**data)


def download(
    api_key: str, bite_number: int, directory: Union[str, "os.PathLike[str]"]
) -> Path:
    """Download a codechalleng.es bite exercise."""
    url = f"https://codechalleng.es/api/bites/downloads/{api_key}/{bite_number}"
    response = requests.get(url)
    response.raise_for_status()

    content_disposition = response.headers["content-disposition"]
    _, params = cgi.parse_header(content_disposition)
    filename = params["filename"]

    directory = Path(directory).resolve()
    extract_dir = (directory / filename).with_suffix("")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
        zip.extractall(extract_dir)

    return extract_dir
