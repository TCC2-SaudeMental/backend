import os
from api.env import get_db_url, settings
from unittest import mock

test_dict = {
    'DB_USER': 'test_user',
    'DB_PASSWORD': 'test_password',
    'DB_HOST': 'test_host',
    'DB_PORT': 'test_port',
    'DB_NAME': 'test_name'
}


def test_get_db_url_default():
    url = get_db_url()
    settings_dict = settings()

    test_url = 'postgresql://user:password@localhost:5432/tcc2'
    assert url == test_url
    assert settings_dict == {'db_url': test_url}


@mock.patch.dict(os.environ, {"DATABASE_URL": "www.url.com/address"})
def test_get_db_url_with_database_url():
    url = get_db_url()
    settings_dict = settings()

    test_url = 'www.url.com/address'
    assert url == test_url
    assert settings_dict == {'db_url': test_url}


@mock.patch.dict(os.environ, test_dict)
def test_get_db_url_with_envs():
    url = get_db_url()
    settings_dict = settings()

    test_url = (
        'postgresql://test_user:test_password@test_host:test_port/test_name'
    )
    assert url == test_url
    assert settings_dict == {'db_url': test_url}
