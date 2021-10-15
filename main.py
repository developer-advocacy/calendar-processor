#!/usr/bin/env python

import datetime
import os
import typing
import time
import googleapiclient.discovery
from googleapiclient.discovery import build

import auth

import pytz


class Calendar(object):

    def __init__(self, service: googleapiclient.discovery.Resource):
        self.service = service

    def read_entries_from(self, this_month: datetime.datetime) -> typing.List[object]:
        return []

    def read_next_n_calendar_entries_from(self, n: int, start: datetime.datetime) -> typing.List[object]:
        now = start.isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=n, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def create_calendar_entry(self,
                              summary: str,
                              location: str,
                              description: str,
                              startdatetime: datetime.datetime,
                              stopdatetime: datetime.datetime,
                              tz: str = None
                              ):
        if tz is not None:
            stopdatetime = stopdatetime.astimezone(pytz.timezone(tz))
            startdatetime = startdatetime.astimezone(pytz.timezone(tz))
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            # Specify timed events using the start.dateTime and end.dateTime fields.
            # For all-day events, use start.date and end.date instead.
            'start': {
                'dateTime': startdatetime.isoformat(),
                'timeZone': tz,
            },
            'end': {
                'dateTime': stopdatetime.isoformat(),
                'timeZone': tz,
            },
            # 'recurrence': [
            #     'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            'attendees': [
                {'email': 'josh@joshlong.com'},
                # {'email': 'bspatz@vmware.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day earlier
                    {'method': 'popup', 'minutes': 10},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')


def main():
    desktop = os.path.join(os.environ['HOME'], 'Desktop', 'google-auth')
    credentials = auth.authenticate(os.path.join(desktop, 'token.json'),
                                    os.path.join(desktop, 'authenticated-token.json'))
    assert credentials is not None, 'the credentials must be valid!'
    service: googleapiclient.discovery.Resource = build('calendar', 'v3', credentials=credentials)

    calendar = Calendar(service)
    tz = pytz.timezone('America/Los_Angeles')
    start = datetime.datetime.now()
    stop = datetime.datetime(year=2021, month=10, day=16, hour=2, minute=2, second=0)
    calendar.create_calendar_entry(
        summary="Partay",
        location='Your Place ',
        description='A chance to hear more about stuff.',
        startdatetime=start,
        stopdatetime=stop
    )
    for event in calendar.read_next_n_calendar_entries_from(20, start):
        #  todo! this fails if u specify a timezone!! DONT do datetime.astimezone()
        print('-' * 100)
        print(event)
        start = event['start'].get('date', event['start'].get('dateTime'))
        print(start, ':', event['summary'])


if __name__ == '__main__':
    main()
