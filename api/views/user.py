from typing import Mapping
from flask import Blueprint, request, g
from . import JSONFormatException, response, error
from api.decorators.auth import auth_decorator
from api.services import ServiceError
from api.services.user import UserService
from api.schemas.user import UserChangeScoreSchema
from marshmallow import ValidationError

user_b = Blueprint(
    'user',
    __name__,
)


@user_b.route('/user/score', methods=['PUT'])
@auth_decorator
def record_score():
    data = request.get_json()
    try:
        if not isinstance(data, Mapping):
            raise JSONFormatException()
        user = g.user

        score_data = UserChangeScoreSchema().load(data)

        message = UserService().change_score(user.id, score_data)

        return response(message)
    except (ValidationError, ServiceError, JSONFormatException) as err:
        return error(400, err.messages)
    except Exception as err:
        return error(500, str(err))
