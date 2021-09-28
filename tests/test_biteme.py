from pathlib import Path

from pytest import raises

import biteme


class TestBiteInfo:
    def test___init__(self) -> None:
        bite = biteme.BiteInfo(
            number=1,
            title="title",
            description="description",
            level="level",
            tags=["tag1", "tag2"],
            free=True,
            score=2,
            function="function",
        )
        assert bite.number == 1
        assert bite.title == "title"
        assert bite.description == "description"
        assert bite.level == "level"
        assert bite.tags == frozenset({"tag1", "tag2"})
        assert bite.free is True
        assert bite.score == 2
        assert bite.function == "function"


def test_get_bite_info() -> None:
    bite = biteme.get_bite_info(1)
    assert bite.number == 1


def test_get_bite_info_raises_for_invalid_bite_number() -> None:
    with raises(IOError):
        biteme.get_bite_info(0)


def test_download_bite(api_key: str, tmp_path: Path) -> None:
    bite_dir = biteme.download_bite(api_key, 1, tmp_path)
    assert bite_dir.is_dir()
    assert bite_dir.stem == "pybites_bite1"


def test_download_bite_raises_for_invalid_bite_number(
    api_key: str, tmp_path: Path
) -> None:
    with raises(IOError):
        biteme.download_bite(api_key, 0, tmp_path)
