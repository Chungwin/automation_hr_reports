import os

from dotenv import load_dotenv
load_dotenv()
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")

from google.oauth2 import service_account
from googleapiclient.discovery import build

#Google Sheets service instance
CLIENT_SECRET_FILE = gsheet_credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)


def write_spreadsheet(sheet_id, list_of_list):
    request = service.spreadsheets().values().update(
                                                    spreadsheetId=sheet_id, 
                                                    range= "Sheet1!A1", 
                                                    valueInputOption="USER_ENTERED",
                                                    body={"values": list_of_list}
                                                    )    
    response = request.execute()
    print('yay!')