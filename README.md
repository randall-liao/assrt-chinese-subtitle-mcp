# 射手网（伪）MCP服务

[English Documentation](README.en.md) | [英文文档](README.en.md)

给射手网（伪） assrt.net 写的 MCP 服务器。

## 项目结构

```text
.
├── .github/
│   └── workflows/          # GitHub Actions CI/CD 配置
├── src/                    # 源码
│   └── main.py
├── tests/                  # 测试
│   └── test_main.py
```

## 技术栈

- **Python:** >= 3.14
- **包管理:** [uv](https://github.com/astral-sh/uv)
- **框架:** `mcp` SDK
- **测试:** `pytest`
- **代码检查/格式化:** `ruff`
- **类型检查:** `pyright`
- **密钥扫描:** `gitleaks`

## 环境配置

1. **装 `uv`**：没装过的看 [这里](https://docs.astral.sh/uv/getting-started/installation/)。

2. **装依赖**：
   ```bash
   uv sync --all-extras --dev
   ```

3. **配 Pre-commit**：
   ```bash
   uv run pre-commit install
   ```
   装完之后，每次 `git commit` 会自动跑代码检查、类型检查和密钥扫描。

## CI/CD

- **Pre-commit**：提交时自动跑 `ruff`、`ruff-format`、`pyright`、`gitleaks`。

- **GitHub Actions**：
  - `PR Checks`：代码格式、Lint、类型检查
  - `Gitleaks`：扫有没有不小心提交的密钥或 Token
