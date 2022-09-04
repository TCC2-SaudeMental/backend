import pytest
from faker import Faker
from api.db import get_engine
from sqlalchemy.orm import Session
from api.models.user import User
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


def test_signup_request(client):

    faker = Faker()

    name = faker.first_name()

    email = faker.last_name() + name + "@gmail.com"

    password = faker.password()

    payload = {
        "name": faker.name(),
        "email": email,
        "password": password,
        "confirm_password": password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 200
    assert response.json['status'] == "success"


def test_signup_empty_name(client):

    faker = Faker()

    name = ""

    email = faker.last_name() + faker.first_name() + "@gmail.com"

    password = faker.password()

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "confirm_password": password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = 'O campo "nome" deve ter no mínimo 2 caracteres'
    assert error_msg in response.json['data']['name']


def test_signup_name_too_long(client):

    faker = Faker()

    name = (
        "Juugemujugemugookonosurikekaijarisugyoonisugyoomasuunraimasufuraimasu"
        "kuunerutokoronisumutokoroyaburaikoojinoburaikoojipaipopaipopaipono"
        "shuuringanshuuringannoguurindaiguurindainoponpokopiinoponpokonaano"
        "choukyuumeinochoosukedeAlcântaraFranciscoAntónioJoãoCarlosXavierde"
        "PaulaMiguelRafaelJoaquimJoséGonzagaPascoalCiprianoSerafim"
    )

    email = faker.last_name() + faker.first_name() + "@gmail.com"

    password = faker.password()

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "confirm_password": password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = 'O campo "nome" deve ter no máximo 255 caracteres'
    assert error_msg in response.json['data']['name']


def test_signup_email_too_long(client):

    faker = Faker()

    name = faker.first_name()

    email = (
        "Juugemujugemugookonosurikekaijarisugyoonisugyoomasuunraimasufuraimasu"
        "kuunerutokoronisumutokoroyaburaikoojinoburaikoojipaipopaipopaipono"
        "shuuringanshuuringannoguurindaiguurindainoponpokopiinoponpokonaano"
        "choukyuumeinochoosukedeAlcântaraFranciscoAntónioJoãoCarlosXavierde"
        "PaulaMiguelRafaelJoaquimJoséGonzagaPascoalCiprianoSerafim"
        "@gmail.com"
    )

    password = faker.password()

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "confirm_password": password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = 'O campo "email" deve ter no máximo 255 caracteres'
    assert error_msg in response.json['data']['email']


def test_signup_invalid_email(client):

    faker = Faker()

    name = faker.first_name()

    email = "@gmail.com"

    password = faker.password()

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "confirm_password": password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"
    assert "O email informado é inválido" in response.json['data']['email']


def test_signup_empty_password(client):

    faker = Faker()

    name = faker.first_name()

    email = faker.last_name() + name + "@gmail.com"

    password = ""

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "confirm_password": password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = 'O campo "senha" deve ter no mínimo 8 caracteres'
    assert error_msg in response.json['data']['password']


def test_signup_password_not_match(client):

    faker = Faker()

    name = faker.first_name()

    email = faker.last_name() + name + "@gmail.com"

    password = faker.password()

    confirm_password = password + "notmatching"

    payload = {
        "name": name,
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = "As senhas informadas não coincidem"
    assert error_msg in response.json['data']['_schema']


def test_signup_json_format_error(client):

    payload = "bad payload"

    response = client.post(
        '/signup',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"


def test_login_valid(client, get_user):

    payload = {"email": get_user.email, "password": "password"}

    response = client.post(
        '/login',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert response.json['data']['token'] is not False


def test_login_invalid_email(client):

    payload = {"email": "invalid@gmail.com", "password": "password"}

    response = client.post(
        '/login',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"
    assert "Credenciais Inválidas" in response.json['data']['login']


def test_login_missing_email(client):

    payload = {"password": "password"}

    response = client.post(
        '/login',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = 'Campo "email", não informado'
    assert error_msg in response.json['data']['email']


def test_login_missing_password(client):

    payload = {
        "email": "email@gmail.com",
    }

    response = client.post(
        '/login',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"

    error_msg = 'Campo "senha", não informado'
    assert error_msg in response.json['data']['password']


def test_login_invalid_password(client, get_user):

    payload = {"email": get_user.email, "password": "invalidpassword"}

    response = client.post(
        '/login',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"
    assert "Credenciais Inválidas" in response.json['data']['login']


def test_login_json_format_error(client, get_user):

    payload = "bad payload"

    response = client.post(
        '/login',
        json=payload,
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
    )

    assert response.status_code == 400
    assert response.json['status'] == "error"


def test_auth_user_success(client, get_user):
    token = sign_jwt(get_user)

    response = client.get(
        '/auth/user',
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json['data']['user']['name'] == 'Mr. Tester'
    assert response.json['data']['user']['email'] == 'tester@email.com'


def test_auth_user_fail(client):
    response = client.get(
        '/auth/user',
        headers={
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": 'bad token'
        }
    )
    assert response.status_code == 401
    assert response.json['status'] == "error"


def test_signup_invalid_method(client):

    response = client.get('/signup')

    assert response.status_code == 405


def test_login_invalid_method(client):

    response = client.get('/login')

    assert response.status_code == 405


def test_auth_user_invalid_method(client):

    response = client.post('/auth/user')

    assert response.status_code == 405
