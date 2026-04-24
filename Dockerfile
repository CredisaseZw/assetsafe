# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:/usr/local/bin:$PATH \
    DJANGO_SETTINGS_MODULE=core.settings \
    PYTHONPATH=/app

# Install uv (prebuilt static binary, no pip bootstrap cost)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Minimal runtime-only OS deps. psycopg2-binary bundles libpq; no build toolchain needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        netcat-openbsd \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for layer caching (only busts when lockfile changes)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
        uv sync --frozen --no-dev --no-install-project

# Copy app code
COPY . .

# Install the project itself (fast; deps already resolved)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

RUN mkdir -p /app/static /app/media /app/logs /app/staticfiles

EXPOSE 8081

# Run directly from the prebuilt virtualenv.
ENTRYPOINT ["python", "/app/entrypoint.py"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8081", "--workers", "3"]
