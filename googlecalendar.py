import datetime
import typing

import googleapiclient.discovery

import pytz


def build_valid_tz(tz: typing.Union[str, datetime.tzinfo]) -> bool:
    assert tz is not None, 'you must provide a value for the timezone'
    ntz = None
    if isinstance(tz, str):
        ntz = pytz.timezone(tz)
    elif isinstance(tz, datetime.tzinfo):
        ntz = tz
    return ntz


class Calendar(object):

    def __init__(self, service: googleapiclient.discovery.Resource):
        self.service = service

    def get_events_between(self,
                           start: datetime.datetime,
                           stop: datetime.datetime,
                           tz: datetime.tzinfo,
                           max_results: int = None) -> typing.List[object]:
        dict_of_args = dict(
            calendarId='primary',
            timeMin=start.astimezone(tz).isoformat(),
            timeMax=stop.astimezone(tz).isoformat(),
            singleEvents=True,
            orderBy='startTime'
        )
        if max_results is not None:
            dict_of_args['maxResults'] = max_results

        events_result = self.service.events().list(**dict_of_args).execute()
        events = events_result.get('items', [])
        return events

    def create_event(self,
                     summary: str,
                     location: str,
                     description: str,
                     startdatetime: datetime.datetime,
                     stopdatetime: datetime.datetime,
                     tz: typing.Union[datetime.tzinfo, str] = None
                     ):
        ntz = None
        if tz is not None:
            stopdatetime = stopdatetime.astimezone(ntz)
            startdatetime = startdatetime.astimezone(ntz)

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            # Specify timed events using the start.dateTime and end.dateTime fields.
            # For all-day events, use start.date and end.date instead.
            'start': {
                'dateTime': startdatetime.isoformat(),
                # 'timeZone': tz,
            },
            'end': {
                'dateTime': stopdatetime.isoformat(),
                # 'timeZone': tz,
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

        return self.service.events().insert(calendarId='primary', body=event).execute()
