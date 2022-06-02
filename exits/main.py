import gsheet_functions
import hibob_api
import pandas as pd

def update():
    api_exit_names = hibob_api.get_api_exits()
    old_exit_names = gsheet_functions.get_old_exit_names()
    difference = list(set(api_exit_names[0]) - set(old_exit_names[0]))

    if len(difference) == 0:
        print('No new exits.')
        
    else:
        print(f'New Exits: {difference}')

        df_api_exits = api_exit_names[1]

        new_leaver_lol = []

        # clean and transform
        for name in difference:
            leaver = df_api_exits.loc[df_api_exits['Full name'] == name].values.tolist()
            leaver = leaver[0]
            leaver = leaver[:-1]
            new_leaver_lol.append(leaver)

        gsheet_functions.insert_rows(new_leaver_lol)
        gsheet_functions.sort_spreadsheet()

update()
