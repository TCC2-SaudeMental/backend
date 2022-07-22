import os
import jwt
from datetime import datetime, timezone, timedelta


class JWTError(Exception):
    message: str

    def __init__(self, message):
        self.message = message


def sign_jwt(user):

    secret = os.getenv('APP_SECRET', 'secret')

    jwt_payload = {
        "id": user.id,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
    }

    return jwt.encode(jwt_payload, secret, algorithm="HS256")


def verify_jwt(token):
    secret = os.getenv('APP_SECRET', 'secret')

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise JWTError('Token expirado')
    except Exception as err:
        raise JWTError(str(err))
