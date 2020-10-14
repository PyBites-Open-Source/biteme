from pathlib import Path

from biteme import BiteID, main

directory = Path.home() / "Documents/GitHub/pybites"
bite_id = BiteID(1)
main(directory, bite_id)
