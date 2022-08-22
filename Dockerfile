FROM python:3.10.5-slim as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app


FROM base as builder

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes -o requirements.txt

RUN poetry export --without-hashes --dev -o dev_requirements.txt

RUN python -m venv /venv

RUN python -m venv /dev_venv

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

RUN /dev_venv/bin/pip install --no-cache-dir -r dev_requirements.txt


FROM base as production

COPY --from=builder /venv /venv

COPY ./api ./api

ENV PATH=/venv/bin:$PATH

CMD gunicorn -b 0.0.0.0:$PORT api.wsgi:app 

FROM base as release

COPY --from=builder /dev_venv /dev_venv

COPY ./api ./api

COPY ./migrations ./migrations

COPY ./alembic.ini ./alembic.ini

ENV PATH=/dev_venv/bin:$PATH   

CMD alembic upgrade head

FROM base as test

COPY --from=builder /dev_venv /dev_venv

COPY ./api ./api

COPY ./tests ./tests

ENV PATH=/dev_venv/bin:$PATH 

CMD pytest -s --cov
