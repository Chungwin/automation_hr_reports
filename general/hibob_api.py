
import os
import requests
from dotenv import load_dotenv
load_dotenv()
report_id = os.getenv("HIBOB_SCRIPT_REPORT_ID")
hibob_token = os.getenv("HIBOB_TOKEN")


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

    print("Report downloaded from HiBob.")
    return list_of_lists
