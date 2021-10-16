#!/usr/bin/env python
import datetime
import os

import pytz

import auth
import dt
from google import sheets, calendar


class Event(object):

    def __str__(self) -> str:
        return f'start: {self.start} stop: {self.stop} time: {self.time} event: "{self.event}" '

    def __init__(self, event: str, start: datetime.datetime, stop: datetime.datetime, time: str) -> None:
        super().__init__()
        self.event: str = event
        self.start: datetime.datetime = start
        self.stop: datetime.datetime = stop
        self.time: str = dt.parse_time(time)


def main():
    scopes: list = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/calendar']
    desktop = os.path.join(os.environ['HOME'], 'Desktop', 'google-auth')
    credentials = auth.authenticate(os.path.join(desktop, 'token.json'),
                                    os.path.join(desktop, 'authenticated-token.json'),
                                    scopes)
    assert credentials is not None, 'the credentials must be valid!'
    sheet_id = os.environ['SHEET_ID']
    my_sheet: sheets.GoogleSheet = sheets.GoogleSheet(credentials, sheet_id)
    my_calendar: calendar.GoogleCalendar = calendar.GoogleCalendar(credentials)
    tz = pytz.timezone('America/Los_Angeles')
    start_date, stop_date = dt.get_current_month_dates()
    rows = my_sheet.read_values('A:X')
    event_header = find_column(rows, 'event')
    start_date_header = find_column(rows, 'start date')
    stop_date_header = find_column(rows, 'end date')
    time_header = find_column(rows, 'time')
    cols = [time_header, event_header, start_date_header, stop_date_header]
    col_width = max(cols) + 1
    rows = [r for r in rows[1:]]
    rows = [r for r in rows if len(r) >= col_width]
    rows = [(row[event_header], row[start_date_header], row[stop_date_header], row[time_header]) for row in rows]
    rows = [Event(event=x[0], start=x[1], stop=x[2], time=x[3]) for x in rows]

    for row in rows:
        print(row)


def find_column(rows: list[object], name: str) -> int:
    ctr = 0
    for c in rows[0]:
        if c.lower() == name.lower():
            return ctr
        ctr += 1
    return -1


if __name__ == '__main__':
    main()
