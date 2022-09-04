import pytest
from api.services.jwt import sign_jwt
from api.db import get_engine
from sqlalchemy.orm import Session
from api.models.user import User


@pytest.fixture
def get_user(test_app):
    with test_app.app_context():
        engine = get_engine()

        user = User(
            name="Mr. Tester",
            email="tester@email.com",
            password="password",
            score=7
        )

        with Session(engine) as session:
            session.add(user)
            session.commit()
            yield user


def test_increase_score_success(client, get_user):
    token = sign_jwt(get_user)

    payload = {"amount": 2}

    response = client.put(
        '/user/score',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {token}'
        }
    )

    positive_message = 'Que ótimo! Torcemos para que você continue bem!'
    assert response.status_code == 200
    assert response.json['data'] == positive_message
    assert response.json['status'] == "success"


def test_decrease_score_success(client, get_user):
    token = sign_jwt(get_user)

    payload = {"amount": -2}

    response = client.put(
        '/user/score',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {token}'
        }
    )

    negative_message = (
        "Que pena... parece que ultimamente você não anda"
        "tão bem, mas pode ser momentâneo. "
        "Procure cuidar de seu corpo e de sua mente, "
        "a próxima vai ser melhor!"
    )
    assert response.status_code == 200
    assert response.json['data'] == negative_message
    assert response.json['status'] == "success"


def test_decrease_score_to_zero_success(client, get_user):
    token = sign_jwt(get_user)

    payload = {"amount": -7}

    response = client.put(
        '/user/score',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {token}'
        }
    )

    negative_message = (
        'As suas respostas andam muito... negativas... '
        'Recomendamos você a procurar a ajuda de um profissional. '
        'Nada substitui o acompanhamento feito por um '
        'psicólogo. Nao tenha vergonha de pedir ajuda!'
    )
    assert response.status_code == 200
    assert response.json['data'] == negative_message
    assert response.json['status'] == "success"


def test_change_score_json_format_error(client, get_user):
    token = sign_jwt(get_user)

    payload = "bad payload"

    response = client.put(
        '/user/score',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f'Bearer {token}'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"


def test_change_score_401(client):

    payload = {"amount": 1}

    response = client.put(
        '/user/score',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": 'Bad token'
        }
    )

    assert response.status_code == 401
    assert response.json['status'] == "error"


def test_change_score_invalid_method(client):

    response = client.get('/user/score')

    assert response.status_code == 405
