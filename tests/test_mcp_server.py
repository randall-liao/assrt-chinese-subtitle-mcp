import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, patch

# Add src to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server import (
    get_subtitle_detail,
    get_similar_subtitles,
    get_user_quota,
    search_subtitles,
)


@pytest.fixture
def mock_client():
    with patch("mcp_server.get_client") as mock_get_client:
        client = AsyncMock()
        mock_get_client.return_value = client
        yield client


@pytest.mark.asyncio
async def test_search_subtitles(mock_client):
    mock_client.search_subtitles.return_value = {"status": 0}

    result = await search_subtitles(
        q="test query", pos=15, cnt=10, is_file=0, no_muxer=0, filelist=0
    )

    assert result == {"status": 0}
    mock_client.search_subtitles.assert_called_once_with(
        q="test query", pos=15, cnt=10, is_file=0, no_muxer=0, filelist=0
    )


@pytest.mark.asyncio
async def test_get_subtitle_detail(mock_client):
    mock_client.get_subtitle_detail.return_value = {"status": 0}
    result = await get_subtitle_detail(123456)
    assert result == {"status": 0}
    mock_client.get_subtitle_detail.assert_called_once_with(123456)


@pytest.mark.asyncio
async def test_get_similar_subtitles(mock_client):
    mock_client.get_similar_subtitles.return_value = {"status": 0}
    result = await get_similar_subtitles(123456)
    assert result == {"status": 0}
    mock_client.get_similar_subtitles.assert_called_once_with(123456)


@pytest.mark.asyncio
async def test_get_user_quota(mock_client):
    mock_client.get_user_quota.return_value = 20
    result = await get_user_quota()
    assert result == 20
    mock_client.get_user_quota.assert_called_once()
