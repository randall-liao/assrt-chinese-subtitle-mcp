with open("src/https_client.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith("def _request"):
        lines[i] = "    async def _request(\n        self, method: str, endpoint: str, params: typing.Optional[dict[str, typing.Any]] = None\n    ) -> dict[str, typing.Any]:\n"
        lines[i+1] = ""
        lines[i+2] = ""
    elif line.strip().startswith("async def search_subtitles"):
        lines[i] = "    async def search_subtitles(\n        self,\n        q: str,\n        pos: int = 0,\n        cnt: int = 15,\n        is_file: int = 0,\n        no_muxer: int = 0,\n        filelist: int = 0,\n    ) -> dict[str, typing.Any]:\n"
        lines[i+1] = ""
        lines[i+2] = ""
        lines[i+3] = ""
        lines[i+4] = ""
        lines[i+5] = ""
        lines[i+6] = ""
        lines[i+7] = ""
    elif line.strip().startswith("async def get_subtitle_detail"):
        lines[i] = "    async def get_subtitle_detail(self, id: int) -> dict[str, typing.Any]:\n"
    elif line.strip().startswith("async def get_similar_subtitles"):
        lines[i] = "    async def get_similar_subtitles(self, id: int) -> dict[str, typing.Any]:\n"
    elif line.strip().startswith("raise AssrtAPIError(status, f\"API error, status code: {status}\")"):
        lines[i] = "            error_msg = data.get(\"msg\") or data.get(\"errmsg\") or f\"API error, status code: {status}\"\n            raise AssrtAPIError(status, error_msg)\n"

with open("src/https_client.py", "w") as f:
    f.writelines(lines)
