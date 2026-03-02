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
    Search for subtitles on assrt.net explicitly returning a list of available subtitle metadata.

    ### Agent Usage Guide
    1. Extract the core movie/show name and season/episode info (e.g., 'Fallout S02E07' from 'Fallout 2024 S02E07 1080p WEB h264-ETHEL') to use as the `q` parameter. Avoid using full release names with muxer info as queries by default, as they may yield zero results.
    2. Review the search results schema to identify the `id` of the desired subtitle.
    3. If the user wants to download a subtitle, you MUST use the `get_subtitle_detail` tool using the `id` obtained from these search results to find the actual download URL. Do not attempt to guess or synthesize the download URL.

    ### Expected Output Schema
    Returns a JSON object with the following structure:
    {
      "status": 0, // 0 means success
      "sub": {
        "subs": [
          {
            "id": 123456, // The 6-digit integer ID of the subtitle (Use this for get_subtitle_detail)
            "native_name": "Original Name",
            "videoname": "Target video name",
            "subtype": "srt/ass/etc",
            "upload_time": "2023-01-01 12:00:00"
          }
        ]
      }
    }

    Args:
        q: The search query string. Must be at least 3 characters long. Use a generalized movie/show name (e.g., "Fallout S02E07") instead of exact video release filenames.
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
    Get detailed information about a subtitle by its ID, including the temporary download link.

    ### Agent Usage Guide
    1. Call this tool using a 6-digit `id` retrieved from `search_subtitles`.
    2. Look for the `url` field in the response to get the download link for the subtitle archive (usually .rar or .zip).
    3. Present the download `url` to the user and warn them that the download link is temporary and generated uniquely for this query.

    ### Expected Output Schema
    Returns a JSON object with the following structure:
    {
      "status": 0, // 0 means success
      "sub": {
        "subs": [
          {
            "id": 123456, // The subtitle ID
            "title": "Subtitle Title",
            "url": "http://file0.assrt.net/download/...", // The download URL for the subtitle archive
            "filelist": [{"f": "filename.srt", "s": "sizeKB", "url": "..."}] // Files inside the archive
          }
        ]
      }
    }

    Args:
        id: The 6-digit integer ID of the subtitle.
    """
    client = get_client()
    return await client.get_subtitle_detail(id)


@mcp.tool()
async def get_similar_subtitles(id: int) -> Dict[str, Any]:
    """
    Get 5 similar subtitles to the given subtitle ID.

    ### Agent Usage Guide
    1. Use this tool if the current subtitle ID does not fully meet the user's needs but is close.
    2. You will need to call `get_subtitle_detail` on the newly discovered IDs to obtain their download links.

    ### Expected Output Schema
    Returns a JSON object containing a list of subtitles in the same schema format as `search_subtitles`.

    Args:
        id: The 6-digit integer ID of the subtitle.
    """
    client = get_client()
    return await client.get_similar_subtitles(id)


@mcp.tool()
async def get_user_quota() -> int:
    """
    Get the remaining user quota (requests per minute) for the ASSRT API.

    ### Expected Output Schema
    Returns an integer representing the remaining API calls allowed in the current minute (e.g., 20).
    """
    client = get_client()
    return await client.get_user_quota()


if __name__ == "__main__":
    mcp.run()
