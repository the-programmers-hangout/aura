FROM python:3.8.6

ENV PYTHONFAULTHANDLER=1 \
   PYTHONUNBUFFERED=1 \
   PYTHONHASHSEED=random \
   PYTHONDONTWRITEBYTECODE=1 \
   # pip:
   PIP_NO_CACHE_DIR=off \
   PIP_DISABLE_PIP_VERSION_CHECK=on \
   PIP_DEFAULT_TIMEOUT=100 \
   # poetry:
   POETRY_VERSION=1.1.4 \
   POETRY_NO_INTERACTION=1 \
   POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN ln -s ~/.poetry/bin/poetry /usr/local/bin/poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev
RUN poetry shell
COPY . /app

CMD poetry run aura