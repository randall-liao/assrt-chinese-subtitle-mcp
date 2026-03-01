with open("tests/test_https_client.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("def mock_env(monkeypatch):") and lines[i-1].startswith("@pytest_asyncio.fixture"):
        lines[i-1] = "@pytest.fixture\n"

with open("tests/test_https_client.py", "w") as f:
    f.writelines(lines)
