FROM python:3.11.2
ENV BOT_NAME=$BOT_NAME

COPY . /.
WORKDIR /.

RUN pip install --without dev poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install
