FROM python:3.8.2

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN ln -s ~/.poetry/bin/poetry /usr/local/bin/poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev
RUN poetry shell
COPY . /app

CMD [ "poetry", "run", "aura"]
