import pathlib

import biteme


class TestBiteInfo:
    def test___init__(self) -> None:
        bite_info = biteme.BiteInfo(
            number=1,
            title="title",
            description="description",
            level="level",
            tags=["tag1", "tag2"],
            free=True,
            score=2,
            function="function",
        )
        assert bite_info.number == 1
        assert bite_info.title == "title"
        assert bite_info.description == "description"
        assert bite_info.level == "level"
        assert bite_info.tags == frozenset({"tag1", "tag2"})
        assert bite_info.free is True
        assert bite_info.score == 2
        assert bite_info.function == "function"


def test_download_bite(api_key: str, tmp_path: pathlib.Path) -> None:
    bite_dir = biteme.download_bite(api_key, 1, tmp_path)
    assert bite_dir.is_dir()
    assert bite_dir.stem == "pybites_bite1"
