# AI Agent Conventions and Project Setup

Welcome to the `assrt-chinese-subtitle-mcp` project! This file serves as a guide for AI LLM agents to understand the project structure, tools, and expected conventions. Please strictly adhere to these guidelines when suggesting or implementing changes.

## 1. Project Overview
- **Name**: `assrt-chinese-subtitle-mcp`
- **Description**: An MCP (Model Context Protocol) server for assrt.net.
- **Language**: Python (>= 3.14)
- **Primary Dependencies**: `mcp`

## 2. Directory Structure
- `src/`: Contains all application source code.
- `tests/`: Contains all test files (powered by `pytest`).
- `.github/workflows/`: CI/CD pipelines (e.g., PR checks, gitleaks).

## 3. Toolchain and Dependency Management
- **Package Manager**: [uv](https://github.com/astral-sh/uv). Use `uv` for all dependency management.
  - *Add dependencies*: `uv add <package>`
  - *Add dev dependencies*: `uv add --dev <package>`
  - *Run commands*: `uv run <command>`

## 4. Code Quality & Formatting
This project strictly enforces code quality via tools initialized in `.pre-commit-config.yaml` and `.github/workflows/pr.yml`.
- **Linter**: `ruff`
  - *Run*: `uv run ruff check .`
  - *Fix*: `uv run ruff check --fix .`
- **Formatter**: `ruff`
  - *Run*: `uv run ruff format .`
- **Type Checker**: `pyright`
  - *Run*: `uv run pyright .`
- **Pre-commit Hooks**: It is assumed that `pre-commit` covers `ruff`, `pyright`, and `gitleaks`.

*Agent Instruction*: ALWAYS ensure `ruff` and `pyright` pass without errors before proposing a final solution.

## 5. Security
- **Secret Scanning**: `gitleaks` is configured both as a pre-commit hook and in `.github/workflows/gitleaks.yml`.
  - *Agent Instruction*: NEVER hardcode API keys, passwords, or tokens in the codebase.

## 6. Testing
- **Framework**: `pytest`
- Tests are located in the `tests/` directory.
- Test files should follow the `test_<name>.py` naming convention.
- If importing from `src/`, append `src/` to `sys.path` to avoid unnecessary package installation overhead.
- *Agent Instruction*: Always write tests for new functions/modules and verify that existing tests pass (`uv run pytest`).

## 7. Version Control & Contribution Workflow
The project follows standard GitHub Flow conventions and branch protection rules:
1. **Branching**: DO NOT modify `main` directly. Always branch out for your work (e.g., `feature/add-foo`, `fix/bug-bar`).
2. **Commit Messages**: Use clear, industry-standard commit messages.
3. **Pull Requests**: Create a Pull Request against the `main` branch. Provide detailed PR comments/descriptions explaining the "why" and "what" of your changes.
4. **CI Checks**: Ensure all CI runs (Lint, Formatter, Typecheck, and Gitleaks) pass.

## Summarized Agent Checklist
When an agent is fulfilling a task, keep this checklist in mind:
- [ ] Code is placed in the `src/` directory.
- [ ] Any test files are added to the `tests/` directory.
- [ ] Dependencies are managed purely via `uv`.
- [ ] Code is formatted with `ruff format`.
- [ ] Code passes `ruff check` and `pyright` cleanly.
- [ ] No secrets are hardcoded (to avoid failing `gitleaks`).
- [ ] Code is pushed to a fresh branch and a PR is created following the contribution workflow.
