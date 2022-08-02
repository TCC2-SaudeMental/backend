from marshmallow import (
    Schema, fields, ValidationError, validates, validates_schema
)


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={'required': 'Campo "email", não informado'}
    )

    password = fields.Str(
        required=True,
        error_messages={'required': 'Campo "senha", não informado'}
    )


class UserRegisterSchema(Schema):
    name = fields.Str(
        required=True,
        error_messages={'required': 'Campo "nome" não informado'}
    )

    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Campo "email", não informado',
            'invalid': 'O email informado é inválido'
        }
    )

    password = fields.Str(
        required=True,
        error_messages={'required': 'Campo "senha", não informado'}
    )

    confirm_password = fields.Str(
        required=True,
        error_messages={'required': 'Campo "confirmar senha", não informado'}
    )

    @validates('name')
    def validate_name(self, value):
        length = len(value)

        if length < 2:
            raise ValidationError(
                'O campo "nome" deve ter no mínimo 2 caracteres'
            )
        elif length > 255:
            raise ValidationError(
                'O campo "nome" deve ter no máximo 255 caracteres'
            )

    @validates('email')
    def validate_email(self, value):
        length = len(value)

        if length > 255:
            raise ValidationError(
                'O campo "email" deve ter no máximo 255 caracteres'
            )

    @validates('password')
    def validate_password(self, value):
        length = len(value)

        if length < 8:
            raise ValidationError(
                'O campo "senha" deve ter no mínimo 8 caracteres'
            )

    @validates_schema
    def passwords_match(self, data, **kwargs):
        if data['password'] != data["confirm_password"]:
            raise ValidationError('As senhas informadas não coincidem')


class UserOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    score = fields.Int()


class UserChangeScoreSchema(Schema):
    amount = fields.Int(
        required=True,
        error_messages={'required': 'Campo "amount", não informado'}
    )
