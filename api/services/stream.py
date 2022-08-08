from datetime import datetime, timedelta
from flask import g
from sqlalchemy.orm import Session
from api.models.stream import Stream
from api.schemas.stream import StreamOutputSchema
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

    @DB_error_resistant
    def get_last_streams_by_period(self, days: int):
        td = timedelta(days)

        today = datetime.today()
        initial_date = today - td

        with Session(g.engine) as session:
            streams = session.query(Stream).filter(
                Stream.stream_date >= initial_date
            )
            return StreamOutputSchema(many=True).dump(streams)
