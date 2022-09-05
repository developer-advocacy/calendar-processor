import datetime
import typing

import dt


class Event(object):

    def __str__(self) -> str:
        return f'start: {self.start} stop: {self.stop} time: {self.time} event: "{self.event}" '

    def __init__(self, event: str,
                 start: typing.Union[datetime.datetime, str],
                 # stop: typing.Union[datetime.datetime, str],
                 time: str) -> None:
        super().__init__()
        self.stop = None
        self.event: str = event
        self.start: datetime.datetime = dt.parse_datetime(start)
        self.time: str = dt.parse_time(time)
        if self.time is not None and self.start is not None:
            event = self
            h, m = [int(a) for a in event.time.split(':')]
            new_dt = datetime.datetime(
                year=event.start.year,
                month=event.start.month,
                day=event.start.day,
                minute=m,
                hour=h
            )
            self.start = new_dt
        if self.start is not None:
            self.stop = self.start + datetime.timedelta(hours=1)