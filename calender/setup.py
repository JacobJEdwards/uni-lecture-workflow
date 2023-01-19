#!/usr/bin/env python

import pickle
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import CREDENTIALS_FILE

# If modifying these scopes, delete the file token.pickle.
SCOPES: list = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if Path('calender/token.pickle').exists():
        with open('calender/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                print('Token invalid - remove token.pickle and try again')
                removePickle()

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=3000)

        # Save the credentials for the next run
        with open('calender/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def removePickle():
    pickle_file = Path.cwd() / 'token.pickle'
    if pickle_file.exists():
        pickle_file.unlink()
