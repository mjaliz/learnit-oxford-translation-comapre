FROM ghcr.io/astral-sh/uv:python3.12-bookworm
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen
COPY . /app/
EXPOSE 8000
CMD [ "uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0" ]