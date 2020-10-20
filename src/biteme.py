from __future__ import annotations

import argparse
import io
import os
import subprocess
import venv
import pathlib
import zipfile

import requests


def download_and_extract(bite_number: int, directory: pathlib.Path) -> pathlib.Path:
    api_key = os.getenv("PYBITES_API_KEY")
    url = f"http://codechalleng.es/api/bites/downloads/{api_key}/{bite_number}"
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(path=directory / f"{bite_number}")
    return directory / f"{bite_number}"


def create_virtual_environment(bite_directory: Path) -> None:
    venv.create(bite_directory / ".venv", with_pip=True, upgrade_deps=True)
    python = bite_directory / ".venv/bin/python"
    subprocess.run([python, "-m", "pip", "install", "pytest"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bite-number", type=int, required=True)
    parser.add_argument("-d", "--directory", type=pathlib.Path, required=True)

    args = parser.parse_args()
    bite_directory = download_and_extract(args.bite_number, args.directory)
    create_virtual_environment(bite_directory)


if __name__ == "__main__":
    main()
