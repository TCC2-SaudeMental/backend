import bcrypt
from flask import g
from datetime import date, timedelta
from operator import itemgetter
from sqlalchemy.orm import Session

from .jwt import sign_jwt
from api.models.user import User

from . import ServiceError
from sqlalchemy.exc import IntegrityError, NoResultFound
from api.decorators.errors import DB_error_resistant

DEFAULT_SCORE = 5


class UserService:

    @DB_error_resistant
    def add_user(self, data):

        name, email, password = itemgetter('name', 'email', 'password')(data)

        try:
            user = User(
                name=name, email=email, password=password, score=DEFAULT_SCORE
            )

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

    @DB_error_resistant
    def change_score(self, id: int, score_data) -> str:
        with Session(g.engine) as session:
            user = session.query(User).get(id)
            if user is None:
                raise ServiceError('Usuário requisitado não existe')

            amount = score_data['amount']
            if (
                user.score >= 14 and amount > 0
                or user.score <= 0 and amount < 0 or user.score + amount > 14
                or user.score + amount < 0
            ):
                pass
            else:
                user.score += amount

            today = date.today()
            td = timedelta(1)
            if user.last_answer and user.last_answer >= today - td:
                user.answer_streak += 1
            else:
                user.answer_streak = 1

            user.last_answer = today

            session.commit()
            if user.score == 0:
                return (
                    'As suas respostas andam muito... negativas... '
                    'Recomendamos você a procurar a ajuda de um profissional. '
                    'Nada substitui o acompanhamento feito por um '
                    'psicólogo. Nao tenha vergonha de pedir ajuda!'
                )
            elif amount >= 0:
                return 'Que ótimo! Torcemos para que você continue bem!'
            else:
                return (
                    "Que pena... parece que ultimamente você não anda"
                    "tão bem, mas pode ser momentâneo. "
                    "Procure cuidar de seu corpo e de sua mente, "
                    "a próxima vai ser melhor!"
                )
