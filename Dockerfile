FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root --no-dev

COPY . /app

CMD ["poetry", "run", "python", "main.py"]
