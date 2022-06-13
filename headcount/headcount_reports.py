
import os
import glob
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from Google import Create_Service

from dotenv import load_dotenv
load_dotenv()
dir_headcount_csvs = os.getenv("DIRECTORY_HEADCOUNT_CSVS")
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")
sreports_gsheet_id = os.getenv("SREPORTS_GSHEET_ID")
gdrive_credentails = os.getenv("GDRIVE_CREDENTIALS_PATH")
gsheet_headcount_id = os.getenv("GSHEET_HEADCOUNT_ID")

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



# Read files in directory
list_of_files = glob.glob(dir_headcount_csvs)

list_of_list = []

# Clean up every file
for file_path in list_of_files:

    df = pd.read_csv(file_path)
    lol = df.values.tolist()
    file_name = os.path.basename(file_path).replace('.csv', 'f')
    report_month = file_name.split(" ")[0]
    report_month = report_month.replace(":", "/")

    for row in lol:
        string_row = []
        string_row.insert(0, report_month)
        for item in row:
            if type(item) == float:
                item = str(item)
                string_row.append(item)
            else:
                string_row.append(item)
        list_of_list.append(string_row)



request = service.spreadsheets().values().update(
                                            spreadsheetId=sreports_gsheet_id, 
                                            range= "headcount!A2", 
                                            valueInputOption="USER_ENTERED",
                                            body={"values": list_of_list}
                                            )
response = request.execute()





def sort_spreadsheet():
        
    requests_body = {
        "requests": [
            {
                "sortRange": {
                    "range": {"sheetId": gsheet_headcount_id, "startRowIndex": 1},
                    "sortSpecs": [
                        {
                            "sortOrder": "ASCENDING",
                            "dimensionIndex": 0
                        },
                        
                        {
                            "sortOrder": "ASCENDING",
                            "dimensionIndex": 2
                        }

                    ]
                }
            }
        ]
    } 

    request = sheet_service.spreadsheets().batchUpdate(spreadsheetId=sreports_gsheet_id, body=requests_body)
    response = request.execute()
    print("Sort done.")


sort_spreadsheet()