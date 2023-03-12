FROM python:3.11.2
ENV BOT_NAME=$BOT_NAME

COPY . /src
WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev
