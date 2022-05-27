import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
report_id = os.getenv("HIBOB_SCRIPT_REPORT_ID")
hibob_token = os.getenv("HIBOB_TOKEN")
gdrive_credentails = os.getenv("GDRIVE_CREDENTIALS_PATH")
gdrive_reports_folder_id = os.getenv("GDRIVE_EMPLOYEE_REPORTS_CSVS_FOLDER_ID")
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")

import requests
import pandas as pd
from Google import Create_Service
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

# Google Drive service instance
CLIENT_SECRET_FILE = gdrive_credentails
API_NAME = "drive"
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

#Google Sheets service instance
SHEETS_CLIENT_SECRET_FILE = gsheet_credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(SHEETS_CLIENT_SECRET_FILE, scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)


def get_hibob_report_csv():
    # Get Data from HiBob
    url = f"https://api.hibob.com/v1/company/reports/{report_id}/download?format=csv"
    headers = {
        "Accept": "application/json",
        "Authorization": f"{hibob_token}"
    }
    response = requests.get(url, headers=headers)

    # Transform
    response_string = response.text
    my_data = [x.split(',') for x in response_string.split('\n')]

    list_of_lists = []

    for row in my_data:
        new_row = ["nan" if value == '' else value for value in row]
        list_of_lists.append(new_row)

    print("Report downloaded and transformed")
    return list_of_lists


def gdrive_holiday_filenames():

    # Request
    request  = service.files().list(q=f"parents = '{gdrive_reports_folder_id}'", pageSize=1000)
    response = request.execute()
    files = response.get('files')
    print(files)
    df = pd.DataFrame(files)
    
    if df.empty:
        print('Gdrive reports folder is empty.')
        return ['empty']
    else:
        file_names_array = df["name"].to_numpy()
        return file_names_array


def create_spreadsheet():
    date_time = datetime.now()
    date_time_string = str( date_time)
    file_metadata = {
        'name': f'{date_time_string}-General-Report',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [f'{gdrive_reports_folder_id}'] 
    }
    request = service.files().create(body=file_metadata)
    response = request.execute()
    sheet_id = response['id']
    return sheet_id 

# MUST INVITE Google Account to folder!!
def write_spreadsheet(sheet_id, list_of_list):
    request = sheets_service.spreadsheets().values().update(
                                                    spreadsheetId=sheet_id, 
                                                    range= "Sheet1!A1", 
                                                    valueInputOption="USER_ENTERED",
                                                    body={"values": list_of_list}
                                                    )    
    response = request.execute()
    print('yay!')


list_of_lists = get_hibob_report_csv()
sheet_id = create_spreadsheet()
write_spreadsheet(sheet_id, list_of_lists)


