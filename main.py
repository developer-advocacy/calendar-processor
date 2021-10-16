#!/usr/bin/env python
import datetime
import os
import pytz
import auth
from google import sheets, calendar

def main():
    scopes: list = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/calendar']
    desktop = os.path.join(os.environ['HOME'], 'Desktop', 'google-auth')
    credentials = auth.authenticate(os.path.join(desktop, 'token.json'),
                                    os.path.join(desktop, 'authenticated-token.json'),
                                    scopes)
    assert credentials is not None, 'the credentials must be valid!'
    my_sheet: sheets.GoogleSheet = sheets.GoogleSheet(credentials, os.environ['SHEET_ID'])
    my_calendar: calendar.GoogleCalendar = calendar.GoogleCalendar(credentials)
    tz = pytz.timezone('America/Los_Angeles')
    start = datetime.datetime(year=2021, month=10, day=15, hour=17, minute=33, second=32)
    stop = datetime.datetime(year=2021, month=10, day=15, hour=19, minute=2, second=0)

    if True:
        for i in range(2):
            new_event = my_calendar.create_event(
                summary='a test event', location='online', description='this will be a fun thing we do',
                stopdatetime=stop, startdatetime=start, tz=tz
            )
            print(f"the new event link: {new_event.get('htmlLink')}")

    for e in my_calendar.get_events_between(start, stop, tz):
        print('-' * 10)
        print(e)
        my_calendar.delete_event(eventid=e['id'])


if __name__ == '__main__':
    main()
