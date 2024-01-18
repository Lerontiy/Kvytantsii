import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from icecream import ic


class GoogleSheets:
    def __init__(self, token_file_name:str = "token.json", credentials_file_name:str = "credentials.json"):
        self.sheets = None     

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]   
        credentials = None
        if os.path.exists(token_file_name):
            credentials = Credentials.from_authorized_user_file(token_file_name, SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file_name, SCOPES)
                credentials = flow.run_local_server(port=0)
                del flow

            with open(token_file_name, "w") as token:
                token.write(credentials.to_json())
        del SCOPES

        service = build("sheets", "v4", credentials=credentials)
        del credentials
        self.sheets = service.spreadsheets()

    def get_values(self, spreadsheed_id: str = "1MJThUytl3meSMUC-aTC9k6Kv-wxegei80BjvHLIxWGo", range: str = "Аркуш1!A2:C61") -> list:
        result = self.sheets.values().get(spreadsheetId=spreadsheed_id, range=range).execute()
        return result.get("values", [])
    
gs = GoogleSheets()

        
        
