import os
import typing

import httpx
from dotenv import load_dotenv

load_dotenv()


class AssrtAPIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"ASSRT API Error {status_code}: {message}")


class AssrtClient:
    def __init__(self, token: typing.Optional[str] = None):
        if token is None:
            token = os.environ.get("ASSRT_API_TOKEN")
        if not token:
            raise ValueError(
                "ASSRT API Token is required. Set ASSRT_API_TOKEN environment variable or pass token to AssrtClient."
            )

        self._token = token
        self.base_url = "https://api.assrt.net"
        self.client = httpx.AsyncClient(
            base_url=self.base_url, headers={"Authorization": f"Bearer {token}"}
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: typing.Optional[dict[str, typing.Any]] = None,
    ) -> dict[str, typing.Any]:
        params = {"token": self._token, **(params or {})}
        response = await self.client.request(method, endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        if status != 0:
            error_msg = (
                data.get("msg")
                or data.get("errmsg")
                or f"API error, status code: {status}"
            )
            raise AssrtAPIError(status, error_msg)
        return data

    async def search_subtitles(
        self,
        q: str,
        pos: int = 0,
        cnt: int = 15,
        is_file: int = 0,
        no_muxer: int = 0,
        filelist: int = 0,
    ) -> dict[str, typing.Any]:
        """
        Search for subtitles. `q` must be at least 3 characters long.
        """
        params = {
            "q": q,
            "pos": pos,
            "cnt": cnt,
            "is_file": is_file,
            "no_muxer": no_muxer,
            "filelist": filelist,
        }
        return await self._request("GET", "/v1/sub/search", params)

    async def iter_search_subtitles(
        self,
        q: str,
        is_file: int = 0,
        no_muxer: int = 0,
        filelist: int = 0,
    ) -> typing.AsyncIterator[dict[str, typing.Any]]:
        """
        Return an async iterator that automatically paginates through search results.
        """
        pos = 0
        cnt = 15
        while True:
            response = await self.search_subtitles(
                q=q,
                pos=pos,
                cnt=cnt,
                is_file=is_file,
                no_muxer=no_muxer,
                filelist=filelist,
            )

            subs = response.get("sub", {}).get("subs", [])
            for sub in subs:
                yield sub

            if len(subs) < cnt:
                break

            pos += cnt

    async def get_subtitle_detail(self, id: int) -> dict[str, typing.Any]:
        """
        Get subtitle detailed information by subtitle ID.
        """
        params = {"id": id}
        return await self._request("GET", "/v1/sub/detail", params)

    async def get_similar_subtitles(self, id: int) -> dict[str, typing.Any]:
        """
        Get similar subtitles.
        """
        params = {"id": id}
        return await self._request("GET", "/v1/sub/similar", params)

    async def get_user_quota(self) -> int:
        """
        Get current user quota.
        """
        data = await self._request("GET", "/v1/user/quota")
        return data["user"]["quota"]

    async def close(self):
        await self.client.aclose()
