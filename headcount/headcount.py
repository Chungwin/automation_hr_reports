import os
import requests
from dotenv import load_dotenv
load_dotenv()
gsheet_credentials = os.getenv("GSHEET_CREDENTIALS_PATH")
report_id = os.getenv("HIBOB_VOLKER_REPORT_ID")
hibob_token = os.getenv("HIBOB_TOKEN")
sreports_gsheet_id = os.getenv("SREPORTS_GSHEET_ID")

from google.oauth2 import service_account
from googleapiclient.discovery import build

#Google Sheets service instance
CLIENT_SECRET_FILE = gsheet_credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)


def get_headcount_report_lol():
    url = f"https://api.hibob.com/v1/company/reports/{report_id}/download?format=csv"
    headers = {
                "Accept": "application/json",
                "Authorization": f"{hibob_token}"
            }

    response = requests.get(url, headers=headers)
    response_string = response.text

    my_data = [x.split(',') for x in response_string.split('\n')]
    list_of_lists = []

    for row in my_data:
        new_row = ["nan" if value == '' else value for value in row]
        list_of_lists.append(new_row)

    return list_of_lists


def update_sreport_general(list_of_list):
    
    request = service.spreadsheets().values().update(
                                                spreadsheetId=sreports_gsheet_id, 
                                                range= "headcount!A1", 
                                                valueInputOption="USER_ENTERED",
                                                body={"values": list_of_list}
                                                )
    response = request.execute()
    print('Sreport updated.')


list_of_list = get_headcount_report_lol()
update_sreport_general(list_of_list)