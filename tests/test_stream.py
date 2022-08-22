import pytest
from datetime import datetime
from api.db import get_engine
from sqlalchemy.orm import Session
from api.models.user import User
from api.models.stream import Stream
from api.services.jwt import sign_jwt


@pytest.fixture
def get_user(test_app):
    with test_app.app_context():
        engine = get_engine()

        user = User(
            name="Mr. Tester", email="tester@email.com", password="password"
        )

        with Session(engine) as session:
            session.add(user)
            session.commit()
            yield user


@pytest.fixture
def get_stream(test_app, get_user):
    with test_app.app_context():
        engine = get_engine()

        now = datetime.now().date()

        stream = Stream(stream_date=now, duration=3600, user_id=get_user.id)

        with Session(engine) as session:
            session.add(stream)
            session.commit()
            yield stream


def test_get_report_success(client, get_user, get_stream):
    token = sign_jwt(get_user)

    response = client.get(
        '/stream/report',
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {token}'
        }
    )

    stream = {
        "duration": get_stream.duration,
        "id": get_stream.id,
        "stream_date": get_stream.stream_date.strftime("%Y-%m-%d")
    }

    assert response.status_code == 200
    assert stream in response.json['data']
    assert response.json['status'] == "success"


def test_get_report_fail(client):

    response = client.get(
        '/stream/report',
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
        }
    )

    assert response.status_code == 401
    assert response.json['status'] == "error"


def test_upload_stream_success(client, get_user):
    token = sign_jwt(get_user)

    payload = {"duration": 3600}

    response = client.post(
        '/stream',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {token}'
        }
    )

    assert response.status_code == 200
    assert response.json['status'] == "success"


def test_upload_stream_error(client):

    payload = {"duration": 3600}

    response = client.post(
        '/stream',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
        }
    )

    assert response.status_code == 401
    assert response.json['status'] == "error"
