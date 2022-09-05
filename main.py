#!/usr/bin/env python
import datetime
import os

import pytz

import auth
import dt
import index
import event
from google import sheets, calendar
import typing
from event import Event

'''
This script automatically downloads everything from my travel spreadsheet, 
then populates my private calendar with dummy calendar entries with reminders so that I 
don't accidentally forget to participate in them.

When I get back on the road I'm going to need to start worrying about the timezones again. Right now I'm assuming all times 
in my calendar are in the same timezone as the events in my spreadsheet. Naturally.  
'''

PREFIX = '::SHEET-CALENDAR-AUTO-SYNC::'


def main():
    scopes: list = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/calendar']
    token_json_fn: str = os.environ['CREDENTIALS_JSON_FN']
    authenticated_token_json_fn: str = os.environ['AUTHENTICATED_CREDENTIALS_JSON_FN']
    credentials = auth.authenticate(token_json_fn, authenticated_token_json_fn, scopes)
    assert credentials is not None, 'the credentials must be valid!'
    sheet_id = os.environ['SHEET_ID']
    my_sheet: sheets.GoogleSheet = sheets.GoogleSheet(credentials, sheet_id)
    my_calendar: calendar.GoogleCalendar = calendar.GoogleCalendar(credentials)
    start_date, stop_date = dt.get_current_month_dates()
    tz = pytz.timezone('America/Los_Angeles')
    print(f'starting synchronization @ {datetime.datetime.utcnow()}')
    rows: list[Event] = read_months_events_from_sheet(my_sheet, start_date, stop_date)
    write_calendar_entries(start_date, stop_date, my_calendar, rows, tz)
    print(f'finishing synchronization @ {datetime.datetime.utcnow()}')


def write_calendar_entries(
        start_date: datetime.datetime,
        stop_date: datetime.datetime,
        my_calendar: calendar.GoogleCalendar,
        google_sheet_entries: list[Event],
        tz: datetime.tzinfo):
    google_calendar_entries = find_google_calendar_entries(
        my_calendar.get_events_between(start_date, stop_date, tz))
    google_calendar_index = {}
    google_sheet_index = {}

    for e in google_calendar_entries:
        google_calendar_index[index.build_google_calendar_entry_index(e)] = e

    for e in google_sheet_entries:
        google_sheet_index[index.build_google_sheet_entry_index(e)] = e

    to_delete = []
    for key in google_calendar_index.keys():
        if key not in google_sheet_index.keys():
            to_delete.append(google_calendar_index[key])

    # 1) figure out which calendar entries are _NOT_ in the new sheet entries and delete them
    for td in to_delete:
        to_delete_id = td['id']
        my_calendar.delete_event(eventid=to_delete_id)
        print('deleted', to_delete_id)

    # 2) write only the new sheet entries which are not in the existing calendar entries
    for tw in google_sheet_entries:
        if index.build_google_sheet_entry_index(tw) not in google_calendar_index.keys():
            e = my_calendar.create_event(tw.event, '', PREFIX, tw.start, tw.stop, tz)
            print('added', e['htmlLink'])
            # print('added', f'"{tw.event}"', '@', tw.start, 'with link', e['htmlLink'])


def find_google_calendar_entries(entries) -> typing.List[object]:
    def is_managed_google_calendar_entry(entry: typing.Dict) -> bool:
        key = 'description'
        return key in entry and PREFIX in entry[key]

    return [a for a in entries if is_managed_google_calendar_entry(a)]


# deprecated
def reset_and_write(existing_calendar_entries, my_calendar, prefix, rows, tz):
    for me in find_google_calendar_entries(existing_calendar_entries):
        my_calendar.delete_event(eventid=me.get('id'))

    for event in rows:
        my_calendar.create_event(
            event.event,
            '',
            prefix,
            event.start,
            event.stop,
            tz
        )


def read_months_events_from_sheet(my_sheet, start_date, stop_date) -> typing.List[Event]:
    def find_column(haystack: list[object], needle: str) -> int:
        ctr = 0
        for c in haystack[0]:
            if c.lower() == needle.lower():
                return ctr
            ctr += 1
        return -1

    rows = my_sheet.read_values('Josh!A:X')
    event_header = find_column(rows, 'event')
    start_date_header = find_column(rows, 'start date')
    stop_date_header = find_column(rows, 'end date')
    time_header = find_column(rows, 'time')
    cols = [time_header, event_header, start_date_header, stop_date_header]
    col_width = max(cols) + 1
    rows = [r for r in rows[1:]]
    rows = [r for r in rows if len(r) >= col_width]
    rows = [(row[event_header], row[start_date_header], row[stop_date_header], row[time_header]) for row in rows]
    rows = [Event(event=x[0], start=x[1], time=x[3]) for x in rows]
    rows = [r for r in rows if r.start is not None]
    rows = [r for r in rows if start_date <= r.start < stop_date]  # this month only!
    return rows


if __name__ == '__main__':
    main()
