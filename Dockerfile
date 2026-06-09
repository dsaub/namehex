FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY uv.lock pyproject.toml /app/
RUN uv venv --clear --force && uv sync
COPY entrypoint.sh alembic alembic.ini pyproject.toml /app/
COPY src/ /app/src/
COPY alembic/ /app/alembic/

EXPOSE 8000

CMD ["bash", "/app/entrypoint.sh"]