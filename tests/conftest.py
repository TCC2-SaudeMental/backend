import pytest
from api import create_app
from api.db import get_engine
from api.models import Base


@pytest.fixture()
def test_app():

    test_app = create_app(testing=True)

    with test_app.app_context():
        engine = get_engine()

        Base.metadata.create_all(engine)

        yield test_app

        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()
