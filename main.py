#!/usr/bin/env python
import datetime
import os

import pytz

import auth
import dt
from google import sheets, calendar
import typing


class Event(object):

    def __str__(self) -> str:
        return f'start: {self.start} stop: {self.stop} time: {self.time} event: "{self.event}" '

    def __init__(self, event: str,
                 start: typing.Union[datetime.datetime, str],
                 stop: typing.Union[datetime.datetime, str],
                 time: str) -> None:
        super().__init__()
        self.event: str = event
        self.start: datetime.datetime = dt.parse_datetime(start)
        self.stop: datetime.datetime = dt.parse_datetime(stop)
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
    start_date, stop_date = dt.get_current_month_dates()
    rows: list[Event] = read_months_events_from_sheet(my_sheet, start_date, stop_date)
    write_calendar_entries(my_sheet, my_calendar, rows)


def write_calendar_entries(
        my_sheet: sheets.GoogleSheet,
        my_calendar: calendar.GoogleCalendar,
        rows: list[Event]):
    tz = pytz.timezone('America/Los_Angeles')
    prefix = 'SHEET-SYNC: '
    for event in rows:
        print(event.event, prefix, event.event, event.start, event.time, tz)


def read_months_events_from_sheet(my_sheet, start_date, stop_date) -> typing.List[Event]:
    def find_column(haystack: list[object], needle: str) -> int:
        ctr = 0
        for c in haystack[0]:
            if c.lower() == needle.lower():
                return ctr
            ctr += 1
        return -1

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
    rows = [r for r in rows if r.start is not None]
    rows = [r for r in rows if start_date <= r.start < stop_date]  # this month only!
    return rows


if __name__ == '__main__':
    main()
