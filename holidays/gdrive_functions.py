
import os
import glob
from urllib.error import HTTPError
from Google import Create_Service
import pandas as pd
import numpy as np

from dotenv import load_dotenv
load_dotenv()
gdrive_csv_folder_id = os.getenv("GDRIVE_HOLIDAY_CSVS_FOLDER_ID")
gdrive_credentails = os.getenv("GDRIVE_CREDENTIALS_PATH")
dir_holiday_csvs= os.getenv("DIRECTORY_HOLIDAY_CSVS")

from googleapiclient.http import MediaFileUpload
import gsheets_functions


# Google Drive service instance
CLIENT_SECRET_FILE = gdrive_credentails
API_NAME = "drive"
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def gdrive_holiday_filenames():
    try:
        # Request
        request  = service.files().list(q=f"parents = '{gdrive_csv_folder_id}'", pageSize=1000)
        response = request.execute()
        files = response.get('files')
        df = pd.DataFrame(files)
        
        if df.empty:
            print('Gdrive folder is empty.')
            return ['empty']
        else:
            file_names_array = df["name"].to_numpy()
            return file_names_array

    except Exception as e:
        print(e)



def update():
    try: 
        # Get latest csv from folder
        list_of_files = glob.glob(dir_holiday_csvs)
        latest_file_path = max(list_of_files, key=os.path.getctime)
        file_name = os.path.basename(latest_file_path).replace('.csv', 'f')
        print(f'Latest csv-file: {file_name}')

        # check if file already exists in gdrive
        file_name_array = gdrive_holiday_filenames()

        if file_name in file_name_array:
            print(f'{file_name} already exists in Gdrive.')
        else:
            print('Initiate new holiday report.')

            # Gdrive request - upload file (archive)
            file_metadata = {
                'name': os.path.basename(latest_file_path).replace('.csv', ''),
                'mimeType': 'application/vnd.google-apps.spreadsheet',
                'parents': [f'{gdrive_csv_folder_id}'] 
            }

            media = MediaFileUpload(filename=latest_file_path, mimetype="text/csvv")
            request = service.files().create(media_body=media, body=file_metadata)
            response = request.execute()
            print(f'New report archived.')

            # Write to sreports-spreadhsete
            gsheets_functions.clear_worksheet()
            list_of_lists = gsheets_functions.transform_to_string_lol(latest_file_path)
            gsheets_functions.update_gsheets(list_of_lists)      

    except Exception as e:
        print(e)
