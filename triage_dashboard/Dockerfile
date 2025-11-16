FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml ./
COPY *.py *.html ./
COPY README.md ./

RUN uv sync

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
