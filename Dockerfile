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

CMD ["pdm", "run", "start"]