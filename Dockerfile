FROM python:3.12-slim

WORKDIR /app

COPY /pyproject.toml /
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without lint,dev

COPY . .
RUN mkdir -p ./static
RUN mkdir -p ./staticfiles

RUN python manage.py collectstatic --noinput