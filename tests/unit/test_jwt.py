import os
import jwt
import pytest
from datetime import datetime, timezone, timedelta
from api.db import get_engine
from sqlalchemy.orm import Session
from api.models.user import User
from api.services.jwt import sign_jwt, verify_jwt, JWTError


@pytest.fixture
def get_user(test_app):
    with test_app.app_context():
        engine = get_engine()

        user = User(
            id=222,
            name="Mr. Tester",
            email="tester@email.com",
            password="password"
        )

        with Session(engine) as session:
            session.add(user)
            session.commit()
            yield user


def test_sign_and_decode_jwt_success(get_user):
    token = sign_jwt(get_user)

    assert type(token) == str

    payload = verify_jwt(token)

    assert payload['id'] == 222


def test_decode_jwt_expired(get_user):
    secret = os.getenv('APP_SECRET', 'secret')

    jwt_payload = {
        "id": get_user.id,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=-1),
    }

    token = jwt.encode(jwt_payload, secret, algorithm="HS256")

    with pytest.raises(JWTError) as expired:
        verify_jwt(token)
        assert str(expired.value) == 'Token expirado'


def test_decode_jwt_invalid():
    with pytest.raises(JWTError):
        verify_jwt('bad token')
