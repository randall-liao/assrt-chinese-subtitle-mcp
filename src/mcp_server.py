import typing
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

from https_client import AssrtClient

mcp = FastMCP("Assrt Subtitle MCP")

_client: typing.Optional[AssrtClient] = None


def get_client() -> AssrtClient:
    global _client
    if _client is None:
        _client = AssrtClient()
    return _client


@mcp.tool()
async def search_subtitles(
    q: str,
    pos: int = 0,
    cnt: int = 15,
    is_file: int = 0,
    no_muxer: int = 0,
    filelist: int = 0,
) -> Dict[str, Any]:
    """
    Search for subtitles on assrt.net with explicit pagination control.

    Args:
        q: The search query string. Must be at least 3 characters long.
        pos: The starting position (offset) for pagination. Use this to fetch the next page.
        cnt: The number of results to return (max 15).
        is_file: If 1, `q` is treated as a video filename without extension.
        no_muxer: If 1, ignores release group and video parameters in `q`.
        filelist: If 1, returns the file list inside the archive.
    """
    client = get_client()
    return await client.search_subtitles(
        q=q, pos=pos, cnt=cnt, is_file=is_file, no_muxer=no_muxer, filelist=filelist
    )


@mcp.tool()
async def get_subtitle_detail(id: int) -> Dict[str, Any]:
    """
    Get detailed information about a subtitle by its ID.

    Args:
        id: The 6-digit integer ID of the subtitle.
    """
    client = get_client()
    return await client.get_subtitle_detail(id)


@mcp.tool()
async def get_similar_subtitles(id: int) -> Dict[str, Any]:
    """
    Get 5 similar subtitles to the given subtitle ID.

    Args:
        id: The 6-digit integer ID of the subtitle.
    """
    client = get_client()
    return await client.get_similar_subtitles(id)


@mcp.tool()
async def get_user_quota() -> int:
    """
    Get the remaining user quota (requests per minute) for the ASSRT API.
    """
    client = get_client()
    return await client.get_user_quota()


if __name__ == "__main__":
    mcp.run()
