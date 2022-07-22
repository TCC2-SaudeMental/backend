from typing import Mapping
from flask import Blueprint, request, g
from . import JSONFormatException, response, error
from api.decorators.auth import auth_decorator
from api.services import ServiceError
from api.services.user import UserService
from api.schemas.user import (
    UserLoginSchema, UserRegisterSchema, UserOutputSchema
)
from marshmallow import ValidationError

auth = Blueprint(
    'auth',
    __name__,
)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        if not isinstance(data, Mapping):
            raise JSONFormatException()

        user = UserLoginSchema().load(data)

        token = UserService().login_user(user)

        return response({'token': token})
    except (ValidationError, ServiceError, JSONFormatException) as err:
        return error(400, err.messages)
    except Exception as err:
        return error(500, str(err))


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        if not isinstance(data, Mapping):
            raise JSONFormatException()

        user = UserRegisterSchema().load(data)

        UserService().add_user(user)

        return response(None)
    except (ValidationError, ServiceError, JSONFormatException) as err:
        return error(400, err.messages)
    except Exception as err:
        return error(500, str(err))


@auth.route('/auth/user', methods=['GET'])
@auth_decorator
def auth_user():
    try:
        user = UserOutputSchema().dump(g.user)
        return response({'user': user})
    except Exception as err:
        return error(500, str(err))
