import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    _password = Column(String)
    score = Column(Integer)

    streams = relationship("Stream")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.hashpw(
            value.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')
