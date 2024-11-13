FROM python:3.12.7-slim

LABEL authors="atrya"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry && \
    poetry install --no-dev

EXPOSE 8000

COPY . ./code

ENTRYPOINT ["poetry", "run", "uvicorn", "src.app.main:create_app", "--workers", "4", "--factory", "--host", "0.0.0.0",  "--port", "8000"]