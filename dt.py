import datetime
import os
import typing


def get_current_month_dates() -> typing.Tuple[datetime.datetime, datetime.datetime]:
    now = datetime.datetime.now()
    month = now.month
    year = now.year

    def calculate_next_month(y: int, m: int) -> typing.Tuple[int, int]:
        if m == 12:
            return y + 1, 1
        return y, m + 1

    start_date = datetime.datetime(year=year, month=month, day=1)
    next_year, next_month = calculate_next_month(year, month)
    stop_date = datetime.datetime(year=next_year, month=next_month, day=1)
    return start_date, stop_date


def parse_datetime(dt: typing.Union[str, datetime.datetime]) -> datetime.datetime:
    if dt is None or dt.strip() == '':
        return None

    if isinstance(dt, str):
        dt = dt.strip()
        parts = [int(a.strip()) for a in dt.split('/')]
        m, d, y = parts

        return datetime.datetime(year=y, month=m, day=d)
    return dt


def parse_time(time: str) -> str:
    return __pad_time(__normalize_times(time))


def __pad_time(time: str) -> str:
    if time is None:
        return None

    def pad_digit(d: str) -> str:
        if len(d) == 1:
            return f'0{d}'
        if len(d) == 2:
            return d

    if len(time) == 4:
        return time
    if ':' in time:
        l, r = time.split(':')
        l = pad_digit(l)
        r = pad_digit(r)
        return f'{l}:{r}'
    else:
        return f'{time}:00'


def __normalize_times(time: str) -> str:
    if time is None or time == '':
        return None
    assert time is not None, 'the time must be non-empty'
    time = time.lower().strip()
    if 'noon' in time:
        return '12:00'
    if 'midnite' in time:
        return '00:00'
    has_numbers = time[:]
    has_numbers = any([a.isdigit() for a in has_numbers])
    if not has_numbers:
        return '00:00'
    keep = ''
    found_number = False
    for c in time[:]:
        is_digit = c.isdigit() or c == ':'
        if is_digit:
            found_number = True
            keep += c
        else:
            if found_number:
                break
    keep = keep.strip()
    parts = keep.split(':')
    parts = [int(x.strip()) for x in parts]
    if any([a is None for a in parts]):
        return None
    if len(parts) == 2:
        return f'{parts[0]}:{parts[1]}'
    elif len(parts) == 1:
        return f'{parts[0]}'
