FROM python:3.10.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV FLASK_ENV development

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN groupadd -g 1000 developer && \
  useradd -r -u 1000 -d /home/developer -m -g developer developer && \
  chown developer:developer -R /app

USER developer

RUN poetry install

COPY . ./

ENTRYPOINT [ "poetry", "run" ]

CMD [ "flask", "run", "--host=0.0.0.0" ]
