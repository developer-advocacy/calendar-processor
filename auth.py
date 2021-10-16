import os
import typing

'''
You need to go to https://console.cloud.google.com/apis/credentials?project=<YOUR_PROJECT> 
and create a new OAuth 2 Client ID, choose "Desktop" application, then download the resulting .json file
'''

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# SCOPES = ['https://www.googleapis.com/auth/calendar']


def obtain_fresh_token(file_name: str, scopes: typing.List[str]) -> Credentials:
    flow = InstalledAppFlow.from_client_secrets_file(file_name, scopes)
    credentials = flow.run_local_server(port=0)
    return credentials


def read_persistent_token(file_name: str) -> Credentials:
    return Credentials.from_authorized_user_file(file_name)


def authenticate(token_json_fn: str = 'token.json',
                 authenticated_token_json_fn: str = 'authenticated.json',
                 scopes: typing.List[str] = []) -> Credentials:
    assert any([os.path.exists(a) for a in [token_json_fn,
                                            authenticated_token_json_fn]]), \
        f'you must have either a valid {token_json_fn} or a valid {authenticated_token_json_fn}'

    credentials: Credentials = None
    if not os.path.exists(authenticated_token_json_fn):
        credentials = obtain_fresh_token(token_json_fn, scopes)
        with open(authenticated_token_json_fn, 'w') as t:
            t.write(credentials.to_json())
            print(f'writing {authenticated_token_json_fn} ')
    credentials = read_persistent_token(authenticated_token_json_fn)
    return credentials
