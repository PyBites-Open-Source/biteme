from __future__ import annotations

import pathlib
import tempfile
import zipfile
from typing import SupportsIndex, SupportsInt, Union

import click


class _PositiveInt(int):
    """A strictly-positive integer."""

    def __new__(
        cls, arg: Union[str, bytes, SupportsInt, SupportsIndex]
    ) -> _PositiveInt:
        value = int(arg)
        if value <= 0:
            # TODO: Write a message for the `ValueError`.
            raise ValueError
        # Not sure why Pylance is upset here.
        return super().__new__(cls, value)  # type: ignore

    def __add__(self, other: int) -> _PositiveInt:
        return type(self)(super().__add__(other))

    def __sub__(self, other: int) -> _PositiveInt:
        return type(self)(super().__sub__(other))

    # TODO: Add other binary dunders?


def _get_zipped_bite(bite_number: int) -> zipfile.Path:
    if bite_number != 1:
        raise RuntimeError
    return zipfile.Path(
        pathlib.Path(__file__).parent / f"pybites_bite{bite_number}.zip"
    )


@click.command()
@click.argument("bite-number", type=_PositiveInt)
def main(bite_number: int) -> None:
    bite_number = _PositiveInt(bite_number)
    zipped_bite = _get_zipped_bite(bite_number)


if __name__ == "__main__":
    main()
