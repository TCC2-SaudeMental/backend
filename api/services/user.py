import bcrypt
from flask import g
from operator import itemgetter
from sqlalchemy.orm import Session

from .jwt import sign_jwt
from api.models.user import User

from . import ServiceError
from sqlalchemy.exc import IntegrityError, NoResultFound
from api.decorators.errors import DB_error_resistant


class UserService:

    @DB_error_resistant
    def add_user(self, data):

        name, email, password = itemgetter('name', 'email', 'password')(data)

        try:
            user = User(name=name, email=email, password=password)

            with Session(g.engine) as session:
                session.add(user)
                session.commit()

        except IntegrityError:
            raise ServiceError({'email': ['O email informado já está em uso']})

    @DB_error_resistant
    def get_user(self, id: int):
        with Session(g.engine) as session:
            user = session.query(User).get(id)
            if user is None:
                raise ServiceError('Usuário requisitado não existe')
            return user

    @DB_error_resistant
    def login_user(self, data):
        email, password = itemgetter('email', 'password')(data)

        try:
            with Session(g.engine) as session:
                user = session.query(User).filter_by(email=email).one()

                match = bcrypt.checkpw(
                    password.encode('utf-8'), user.password.encode('utf-8')
                )
                if not match:
                    raise ServiceError({'login': ['Credenciais Inválidas']})

                token = sign_jwt(user)
                return token

        except NoResultFound:
            raise ServiceError({'login': ['Credenciais Inválidas']})
