# TCC2

[![Build](https://github.com/TCC2-SaudeMental/backend/actions/workflows/main.yml/badge.svg)](https://github.com/TCC2-SaudeMental/backend/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/de4e934d6d88be4f43be/maintainability)](https://codeclimate.com/github/TCC2-SaudeMental/backend/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/de4e934d6d88be4f43be/test_coverage)](https://codeclimate.com/github/TCC2-SaudeMental/backend/test_coverage)

## Setup
In order to run the project you must have one of the following installed:
- [Poetry](https://python-poetry.org/)
- [Docker & Docker-Compose](https://docs.docker.com/)

### Poetry 📝
To run the project using poetry use the following commands:
```
$ poetry install
$ poetry run alembic upgrade head
$ poetry run flask run
```

### Docker 🐋
To run the project using Docker use the following commands:
```
$ docker-compose build api
$ docker-compose up -d db
$ docker-compose run --rm api poetry run alembic upgrade head
$ docker-compose up api
```