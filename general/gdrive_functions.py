import os

from dotenv import load_dotenv
load_dotenv()
gdrive_credentails = os.getenv("GDRIVE_CREDENTIALS_PATH")
gdrive_reports_folder_id = os.getenv("GDRIVE_EMPLOYEE_REPORTS_CSVS_FOLDER_ID")

from Google import Create_Service
import pandas as pd
from datetime import datetime

# Google Drive service instance
CLIENT_SECRET_FILE = gdrive_credentails
API_NAME = "drive"
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def get_latest_report_date():

    # Request
    request  = service.files().list(q=f"parents = '{gdrive_reports_folder_id}'", pageSize=1000)
    response = request.execute()
    files = response.get('files')

    df = pd.DataFrame(files)
    
    if df.empty:
        print('Gdrive reports folder is empty.')
        return ['empty']
    else:
        file_names_array = df["name"].to_numpy()
        
        names_list = []
        date_list = []

        for file_name in file_names_array:
            name_split = file_name.split(" ")
            names_list.append(name_split[0])

        for name in names_list:
            date_time_string = name
            date_time_obj = datetime.strptime(date_time_string, '%Y-%m-%d')
            date_list.append(date_time_obj)

        latest_report_date = max(date_list)
        return latest_report_date


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