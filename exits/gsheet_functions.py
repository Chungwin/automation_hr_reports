import os

from dotenv import load_dotenv
load_dotenv()
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")
sreports_gsheet_id = os.getenv("SREPORTS_GSHEET_ID")
gdrive_credentails = os.getenv("GDRIVE_CREDENTIALS_PATH")

from google.oauth2 import service_account
from googleapiclient.discovery import build
from Google import Create_Service

import pandas as pd
import numpy as np

#Google Sheets service instance
CLIENT_SECRET_FILE = gsheet_credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SREPORT_SECRET = gdrive_credentails
API_NAME = "sheets"
API_VERSION = "v4"
sheet_service = Create_Service(SREPORT_SECRET, API_NAME, API_VERSION, SCOPES)


def insert_rows(new_leaver_lol):
    

    request = service.spreadsheets().values().append(
                                                    spreadsheetId=sreports_gsheet_id, 
                                                    range="exits!A:U", 
                                                    valueInputOption="USER_ENTERED",
                                                    body={"values": new_leaver_lol})
    response = request.execute()
    print('Append done.')


def get_old_exit_names():
    try:
        # Read to dataframe
        request = service.spreadsheets().values().get(spreadsheetId=sreports_gsheet_id, range="exits!A:AC")
        response = request.execute()
        values_lol = response["values"]
        df = pd.DataFrame(values_lol)
        
        # Make first row to header
        df.columns = df.iloc[0] 
        df = df[1:]
        df.head()

        df = df.sort_values(by="Termination date", ascending=False)
        a = ['nan', None]
        df = df[~df['Termination date'].isin(a)]
        
        exit_names_sheet = df["Full name"].to_list()
        return exit_names_sheet, df
       
    except Exception as e:
        print(e)       


def sort_spreadsheet():
        
    requests_body = {
        "requests": [
            {
                "sortRange": {
                    "range": {"sheetId": "1430879643"},
                    "sortSpecs": [
                        {
                            "sortOrder": "DESCENDING",
                            "dimensionIndex": 8
                        }
                    ]
                }
            }
        ]
    } 

    request = sheet_service.spreadsheets().batchUpdate(spreadsheetId=sreports_gsheet_id, body=requests_body)
    response = request.execute()
    print("Sort done.")