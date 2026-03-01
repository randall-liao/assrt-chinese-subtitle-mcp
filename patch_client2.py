with open("src/https_client.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == ") -> dict:":
        lines[i] = ""
    elif line.strip().startswith("self, method: str, endpoint: str, params: typing.Optional[dict] = None"):
        lines[i] = "        self, method: str, endpoint: str, params: typing.Optional[dict[str, typing.Any]] = None\n    ) -> dict[str, typing.Any]:\n"
        lines[i+1] = ""

with open("src/https_client.py", "w") as f:
    f.writelines(lines)
