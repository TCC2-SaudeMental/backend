import os


def get_db_url():
    database_url: str = os.environ.get('DATABASE_URL', '')
    if not database_url:
        user = os.environ.get('DB_USER', 'user')
        password = os.environ.get('DB_PASSWORD', 'password')
        host = os.environ.get('DB_HOST', 'localhost')
        port = os.environ.get('DB_PORT', '5432')
        location = os.environ.get('DB_NAME', 'tcc2')

        database_url = (
            f"postgresql://{user}:{password}@{host}:{port}/{location}"
        )

    return database_url.replace('postgres://', 'postgresql://')


def settings():
    return {
        'db_url': get_db_url(),
    }
