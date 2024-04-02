
import os
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.gdch_credentials import ServiceAccountCredentials
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authorize_google_sheets():
    creds = None
    #with open('./service_account.json') as f:
    #    creds_dict = json.load(f)
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        creds = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)
    
    return build('sheets', 'v4', credentials=creds)

def read_google_sheets(service, spreadsheet_id, range_name):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values
