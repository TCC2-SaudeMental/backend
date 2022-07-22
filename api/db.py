from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from .env import settings


def get_engine():
    database_url: str
    if current_app.testing:
        database_url = 'sqlite:///test.db'
    else:
        database_url = settings()['db_url']

    engine = create_engine(database_url, echo=False, future=True)

    return engine


Base = declarative_base()
