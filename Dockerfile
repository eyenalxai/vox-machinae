FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pdm

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./pdm.lock /code/pdm.lock
RUN pdm install

COPY ./app /code/app
COPY ./main.py /code/main.py

ENV OPENAI_TOKEN ${OPENAI_TOKEN}
ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
ENV ALLOWED_USER_IDS ${ALLOWED_USER_IDS}
ENV POLL_TYPE ${POLL_TYPE}
ENV DOMAIN ${DOMAIN}
ENV PORT ${PORT}

ARG EXPOSE_PORT=${PORT}
EXPOSE ${EXPOSE_PORT}

CMD ["pdm", "run", "start"]