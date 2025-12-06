FROM python:3.12-slim

WORKDIR /app
COPY .python-version pyproject.toml ./
RUN pip install uv

RUN uv sync

COPY ./src ./src

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
