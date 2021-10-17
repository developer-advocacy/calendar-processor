'''

Provides routines to capture a hash for calendar
entries in the spreadsheet and in Google Calendar
'''

import datetime
import event


def index(description: str, year: int, month: int, day: int, hour: int, minute: int, tz: str) -> str:
    return f'{description}{year}{month}{day}{hour}{minute}'.lower()


def build_google_sheet_entry_index(nce: event.Event):
    description = compress_string(nce.event)
    start = nce.start
    return index(description, start.year, start.month, start.day, start.hour, start.minute, start.tzname())


def build_google_calendar_entry_index(mce: dict):
    description: str = compress_string(mce['summary'])
    start: str = mce['start']['dateTime']
    start_dt: datetime.datetime = datetime.datetime.fromisoformat(start)
    return index(description, start_dt.year, start_dt.month, start_dt.day,
                 start_dt.hour, start_dt.minute, start_dt.tzname())


def compress_string(input: str) -> str:
    keep = ''
    for c in input[:]:
        if c.isalnum():
            keep += c
    return keep.strip()
