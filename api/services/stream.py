from datetime import datetime
from flask import g
from api.models.stream import Stream
from sqlalchemy.orm import Session
from api.decorators.errors import DB_error_resistant


class StreamService:

    @DB_error_resistant
    def record_stream(self, data):
        duration: int = data['duration']

        with Session(g.engine) as session:
            now = datetime.now().date()

            stream = Stream(
                stream_date=now, duration=duration, user_id=g.user.id
            )
            session.add(stream)
            session.commit()
