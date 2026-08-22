# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements/ ./requirements/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --wheel-dir=/wheels -r requirements/production.txt

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TEMPLATE_DEV=prod

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd libpq5 gosu \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser
WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

RUN mkdir -p /app/logs /app/static /app/media /app/assets \
    && chown -R appuser:appuser /app/logs /app/static /app/media /app/assets

COPY --chown=appuser:appuser ./src ./src
COPY --chmod=755 docker/entrypoint.sh /entrypoint.sh
# Defends against CRLF line endings sneaking in via a Windows checkout that
# predates the .gitattributes eol=lf fix (breaks the #!/bin/sh shebang).
RUN sed -i 's/\r$//' /entrypoint.sh
WORKDIR /app/src

ENTRYPOINT ["/entrypoint.sh"]