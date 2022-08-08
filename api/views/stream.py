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


@stream_b.route('/stream/report', methods=['GET'])
@auth_decorator
def get_report():

    try:
        args = request.args.to_dict()
        days = args['days'] if 'days' in args else '7'
        days = int(days)

        streams = StreamService().get_last_streams_by_period(days)

        return response(streams)
    except ValueError:
        return error(400, 'Days must be an integer')
    except Exception as err:
        return error(500, str(err))
