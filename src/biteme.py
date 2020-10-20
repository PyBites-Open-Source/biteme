from __future__ import annotations

import argparse
import io
import os
import subprocess
import venv
import pathlib
import zipfile

import types
import requests


def download_and_extract(
    bite_number: int, root_directory: pathlib.Path
) -> pathlib.Path:
    bite_directory = root_directory / f"{bite_number}"
    api_key = os.getenv("PYBITES_API_KEY")
    url = f"http://codechalleng.es/api/bites/downloads/{api_key}/{bite_number}"
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(path=bite_directory)
    return bite_directory


class BiteEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context: types.SimpleNamespace) -> None:
        python = pathlib.Path(context.env_dir) / "bin/python"
        subprocess.run([python, "-m", "pip", "install", "pytest"])


def create_virtual_environment(bite_directory: pathlib.Path) -> None:
    builder = BiteEnvBuilder(with_pip=True, upgrade_deps=True)
    builder.create(bite_directory / ".venv")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bite-number", type=int, required=True)
    parser.add_argument("-d", "--directory", type=pathlib.Path, required=True)

    args = parser.parse_args()
    bite_directory = download_and_extract(args.bite_number, args.directory)
    create_virtual_environment(bite_directory)


if __name__ == "__main__":
    main()
