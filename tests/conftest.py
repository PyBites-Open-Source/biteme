from pytest import fixture


@fixture
def api_key() -> str:
    return "biteme-api-key"
