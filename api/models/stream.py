from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True)
    stream_date = Column(Date)
    duration = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="streams")
