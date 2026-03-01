# assrt-chinese-subtitle-mcp

[中文文档](README.md) | Read in Chinese

An MCP (Model Context Protocol) server for assrt.net.

## Project Structure

```text
.
├── .github/
│   └── workflows/          # GitHub Actions CI/CD pipelines
├── src/                    # Application source code
│   └── main.py             # Main server logic
├── tests/                  # Test suite
│   └── test_main.py
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── protection.json         # GitHub branch protection rules
├── pyproject.toml          # Project metadata and configurations
├── uv.lock                 # Exact dependency lockfile
├── README.md               # Project documentation (Chinese)
└── README.en.md            # Project documentation (English)
```

## Technologies & Tools

- **Python:** >= 3.14
- **Package Manager:** [uv](https://github.com/astral-sh/uv)
- **Framework:** `mcp` SDK (Model Context Protocol)
- **Testing:** `pytest`
- **Linting & Formatting:** `ruff`
- **Type Checking:** `pyright`
- **Security:** `gitleaks` (Secret scanning)

## Development Setup

1. **Install `uv`**: If you haven't already, install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. **Setup virtual environment & install dependencies**:
   ```bash
   uv sync --all-extras --dev
   ```
3. **Install Pre-commit Hooks**:
   ```bash
   uv run pre-commit install
   ```
   *Note: This ensures all linters, type checkers, and `gitleaks` run correctly before you commit.*

## CI/CD and Quality Assurance

- **Pre-commit Hooks:** Automatically runs `ruff`, `ruff-format`, `pyright`, and `gitleaks` on every commit.
- **GitHub Actions:**
  - `PR Checks`: Verifies code formatting, lints with `ruff`, and checks types with `pyright`.
  - `Gitleaks`: Scans code for secrets/API keys to prevent accidental leaks.
- **Branch Protection:** Configurations mapped in `protection.json`, requiring `Gitleaks` and `Lint, Format, and Typecheck` to pass before merging into `main`.
