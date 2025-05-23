# This file is used to setup the google calendar API
# It is used in the update_calendar.py file
# The code is taken from: https://aakash-roy.medium.com/calendar-automation-with-python-using-google-calendar-api-and-oauth2-authorization-system-1e263655c079

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# You can change the scope of the application, make sure to delete token.pickle file first
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'config/credentials.json'     # Give path to your credentials.json file


def get_calendar_service():

    cred = None

    '''
    The file token.pickle stores the user's access and refresh tokens, and is created automatically when
    the authorization flow completes for the first time. In other words when the user give access to this 
    channel
    '''

    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            cred = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(cred, token)
    service = build('calendar','v3',credentials=cred)
    return service