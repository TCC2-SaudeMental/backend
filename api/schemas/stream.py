from marshmallow import (
    Schema,
    fields,
)


class StreamInputSchema(Schema):
    duration = fields.Int(
        required=True,
        error_messages={'required': 'Campo "duração", não informado'}
    )
