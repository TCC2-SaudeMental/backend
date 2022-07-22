from functools import wraps
from flask import request, g
from api.services.jwt import verify_jwt, JWTError
from api.services.user import UserService
from api.services import ServiceError
from api.views import error


def auth_decorator(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get('Authorization') or ''
            if not token.startswith("Bearer "):
                return error(401, 'Token inválido')

            payload = verify_jwt(token[7:])
            user = UserService().get_user(payload['id'])

            g.user = user

            return func(*args, **kwargs)
        except (ServiceError, JWTError):
            return error(401, 'Token inválido')

    return decorated_function
