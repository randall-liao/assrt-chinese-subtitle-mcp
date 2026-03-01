with open("src/https_client.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith("self.client = httpx.AsyncClient("):
        lines[i] = "        self.client = httpx.AsyncClient(base_url=self.base_url)\n"
    elif line.strip().startswith("base_url=self.base_url, headers={\"Authorization\": f\"Bearer {token}\"}"):
        lines[i] = ""
    elif line.strip().startswith("self.base_url = \"https://api.assrt.net\""):
        lines.insert(i, "        self._token = token\n")
        break

for i, line in enumerate(lines):
    if line.strip().startswith("response = await self.client.request(method, endpoint, params=params)"):
        lines.insert(i, "        params = {\"token\": self._token, **(params or {})}\n")
        break

with open("src/https_client.py", "w") as f:
    f.writelines(lines)
