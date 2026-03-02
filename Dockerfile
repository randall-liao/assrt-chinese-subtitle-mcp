FROM python:3.14-slim

# Copy the uv installer from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Set up environment variables for uv and virtualenv
ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_COMPILE_BYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy pyproject configurations
COPY pyproject.toml uv.lock ./

# Install project dependencies without the code itself (for layer caching)
RUN uv sync --frozen --no-install-project --no-dev

# Copy only the /src directory (as requested)
COPY src ./src

# Sync again to install the project itself
RUN uv sync --frozen --no-dev

# The Docker image entrypoint is the main Python script running the FastMCP server
ENTRYPOINT ["python", "/app/src/mcp_server.py"]
