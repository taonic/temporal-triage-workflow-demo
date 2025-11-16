FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml ./
COPY *.py ./
COPY README.md ./

RUN uv sync

EXPOSE 6001

CMD ["uv", "run", "python", "main.py"]
