import sys
from pathlib import Path
import pytest
import pytest_asyncio
import respx
import httpx

# Add src to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from https_client import AssrtClient, AssrtAPIError


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("ASSRT_API_TOKEN", "test_token")


@pytest_asyncio.fixture
async def client(mock_env):
    client = AssrtClient()
    yield client
    await client.close()


def test_missing_token(monkeypatch):
    monkeypatch.delenv("ASSRT_API_TOKEN", raising=False)
    with pytest.raises(ValueError, match="ASSRT API Token is required"):
        AssrtClient()


@pytest.mark.asyncio
@respx.mock
async def test_search_subtitles(client):
    mock_response = {
        "status": 0,
        "sub": {
            "subs": [{"id": 123, "native_name": "Test Sub"}],
            "action": "search",
            "keyword": "test",
            "result": "succeed",
        },
    }

    route = respx.get("https://api.assrt.net/v1/sub/search").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await client.search_subtitles("test", cnt=1, is_file=1)

    assert route.called
    assert (
        route.calls.last.request.url.query.decode("utf-8")
        == "q=test&pos=0&cnt=1&is_file=1&no_muxer=0&filelist=0"
    )
    assert result == mock_response


@pytest.mark.asyncio
@respx.mock
async def test_get_subtitle_detail(client):
    mock_response = {
        "status": 0,
        "sub": {
            "result": "succeed",
            "action": "detail",
            "subs": [{"id": 123, "filename": "test.srt"}],
        },
    }

    route = respx.get("https://api.assrt.net/v1/sub/detail").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await client.get_subtitle_detail(123)

    assert route.called
    assert route.calls.last.request.url.query.decode("utf-8") == "id=123"
    assert result == mock_response


@pytest.mark.asyncio
@respx.mock
async def test_get_similar_subtitles(client):
    mock_response = {
        "status": 0,
        "sub": {
            "result": "succeed",
            "action": "similar",
            "subs": [{"id": 456, "native_name": "Similar Sub"}],
        },
    }

    route = respx.get("https://api.assrt.net/v1/sub/similar").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await client.get_similar_subtitles(123)

    assert route.called
    assert route.calls.last.request.url.query.decode("utf-8") == "id=123"
    assert result == mock_response


@pytest.mark.asyncio
@respx.mock
async def test_get_user_quota(client):
    mock_response = {
        "status": 0,
        "user": {"result": "succeed", "action": "quota", "quota": 20},
    }

    route = respx.get("https://api.assrt.net/v1/user/quota").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await client.get_user_quota()

    assert route.called
    assert result == 20


@pytest.mark.asyncio
@respx.mock
async def test_api_error(client):
    mock_response = {"status": 101, "msg": "length of keyword must be longer than 3"}

    route = respx.get("https://api.assrt.net/v1/sub/search").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    with pytest.raises(AssrtAPIError) as exc_info:
        await client.search_subtitles("te")

    assert route.called
    assert exc_info.value.status_code == 101
    assert "status code: 101" in exc_info.value.message
