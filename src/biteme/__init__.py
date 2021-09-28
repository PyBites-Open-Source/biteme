import importlib.metadata
from typing import Final

from .bites import BiteInfo as BiteInfo
from .bites import download_bite as download_bite
from .bites import get_bite_info as get_bite_info
from .cli import cli as cli

__version__: Final[str] = importlib.metadata.version(__package__)
