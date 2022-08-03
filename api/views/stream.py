from typing import Mapping
from flask import Blueprint, request
from . import JSONFormatException, response, error
from api.decorators.auth import auth_decorator
from api.services.stream import StreamService
from api.schemas.stream import StreamInputSchema
from marshmallow import ValidationError

stream_b = Blueprint(
    'stream',
    __name__,
)


@stream_b.route('/stream', methods=['POST'])
@auth_decorator
def stream_duration():
    data = request.get_json()
    try:
        if not isinstance(data, Mapping):
            raise JSONFormatException()

        stream = StreamInputSchema().load(data)

        StreamService().record_stream(stream)

        return response(None)
    except (ValidationError, JSONFormatException) as err:
        return error(400, err.messages)
    except Exception as err:
        return error(500, str(err))
