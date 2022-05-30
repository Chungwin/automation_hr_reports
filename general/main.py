import datetime
import hibob_api
import gdrive_functions
import gsheets_functions


# Comparing Dates
def update(latest_report_date):
    now = datetime.datetime.now()
    now_str = str(now)
    date = now_str.split(" ")
    today_date = datetime.datetime.strptime(date[0], '%Y-%m-%d')

    if (latest_report_date >= today_date):
        print('You already did an update today.')
    else:
        print('Initiate new General report.')

        # Archieve to folder
        list_of_lists = hibob_api.get_hibob_report_csv()
        new_sheet_id = gdrive_functions.create_spreadsheet()
        gsheets_functions.archive_spreadsheet(new_sheet_id, list_of_lists)

        # Update Sreports
        gsheets_functions.clear_worksheet()
        gsheets_functions.update_sreport_general(list_of_lists)


latest_report_date = gdrive_functions.get_latest_report_date()
update(latest_report_date)




