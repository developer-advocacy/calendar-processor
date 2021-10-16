import os.path
import os.path
import pickle

import googleapiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleSheet(object):
    USER_ENTERED = 'USER_ENTERED'
    INPUT_VALUE_OPTION_UNSPECIFIED = 'INPUT_VALUE_OPTION_UNSPECIFIED'
    RAW = 'RAW'

    ## todo can this logic for obtainng a token be extracted
    #  todo out across the two different clients?
    @staticmethod
    def _obtain_token(credentials_config_str: str, pickle_path_fn: str) -> Credentials:
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials: Credentials = None
        if os.path.exists(pickle_path_fn):
            with open(pickle_path_fn, 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(credentials_config_str, scopes)
                credentials = flow.run_local_server(port=0)
                with open(pickle_path_fn, 'wb') as token:
                    pickle.dump(credentials, token)
        return credentials

    def write_values(self, spreadsheet_range: str, input_option: str, values: list):
        body = {'values': values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.id,
            range=spreadsheet_range,
            valueInputOption=input_option,
            body=body) \
            .execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        return result

    def read_values(self, spreadsheet_range: str) -> list:
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.id, range=spreadsheet_range).execute()
        return result.get('values', [])

    def __init__(self, credentials: str, spreadsheet_id: str):
        assert credentials is not None, 'the credentials must be valid'
        assert spreadsheet_id is not None, 'the spreadsheet_id must be valid'
        self.service: googleapiclient.discovery.Resource = build('sheets', 'v4',
                                                                 credentials=credentials)
        self.id = spreadsheet_id
