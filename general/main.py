import datetime
import hibob_api
import gdrive_functions
import gsheets_functions


list_of_lists = hibob_api.get_hibob_report_csv()
sheet_id = gdrive_functions.create_spreadsheet()
gsheets_functions.write_spreadsheet(sheet_id, list_of_lists)

def compare_dates(latest_report_datetime):
    now = datetime.datetime.now()
    now_str = str(now)
    date = now_str.split(" ")
    today_date = datetime.datetime.strptime(date[0], '%Y-%m-%d')

    if (latest_report_datetime > today_date):
        print('You are very uptodate')
    else:
        print('Initiate new report.')

