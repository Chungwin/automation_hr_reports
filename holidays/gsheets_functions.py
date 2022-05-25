import os
from Google import Create_Service
from googleapiclient.discovery import build
from google.oauth2 import service_account

from dotenv import load_dotenv
load_dotenv()
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")
sreports_gsheet_id = os.getenv("SREPORTS_GSHEET_ID")

import pandas as pd

#Google Sheets service instance
CLIENT_SECRET_FILE = gsheet_credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)


def clear_worksheet(): 
    request = service.spreadsheets().values().clear(spreadsheetId=sreports_gsheet_id, range="holidays!1:1000")
    response = request.execute()


def transform_to_string_lol(latest_file_path):
    df = pd.read_csv (latest_file_path)
    lol = df.values.tolist()
    list_of_list = []
    headers = ['Display name', 'Department', 'Business Unit', 'Current policy', 'Current balance', 'Taken this cycle', 'Amount accrued this cycle', 'Accrual effective date', 'Booked before end of cycle', 'Start date', 'Reports to', 'YOS allowance increase', 'Termination date', 'Site']
    list_of_list.append(headers)

    for row in lol:
        string_row = []
        for item in row:
            if type(item) == float:
                item = str(item)
                string_row.append(item)
            else:
                string_row.append(item)
        list_of_list.append(string_row)

    return list_of_list


def update_gsheets(list_of_list):
    request = service.spreadsheets().values().update(
                                                spreadsheetId=sreports_gsheet_id, 
                                                range= "holidays!A1", 
                                                valueInputOption="USER_ENTERED",
                                                body={"values": list_of_list}
                                                )
    response = request.execute()
    print('Sreport (Holidays) successfully updated.')
                    