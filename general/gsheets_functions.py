import os

from dotenv import load_dotenv
load_dotenv()
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")
sreports_gsheet_id = os.getenv("SREPORTS_GSHEET_ID")

from google.oauth2 import service_account
from googleapiclient.discovery import build

#Google Sheets service instance
CLIENT_SECRET_FILE = gsheet_credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)


def archive_spreadsheet(new_sheet_id, list_of_list):
    request = service.spreadsheets().values().update(
                                                    spreadsheetId=new_sheet_id, 
                                                    range= "Sheet1!A1", 
                                                    valueInputOption="USER_ENTERED",
                                                    body={"values": list_of_list}
                                                    )    
    response = request.execute()
    print('Report archived.')


def clear_worksheet():
    request = service.spreadsheets().values().clear(spreadsheetId=sreports_gsheet_id, range="general!1:1000")
    response = request.execute()


def update_sreport_general(list_of_list):
    request = service.spreadsheets().values().update(
                                                spreadsheetId=sreports_gsheet_id, 
                                                range= "general!A1", 
                                                valueInputOption="USER_ENTERED",
                                                body={"values": list_of_list}
                                                )
    response = request.execute()
    print('Sreport updated.')