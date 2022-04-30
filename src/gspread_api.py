import gspread
#import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import os

def get_worksheet_api_service():
    """
    This method is used to get google spread sheet api service

    Returns:
        Object: worksheet object
    """

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.dirname(__file__),'t-skyline-347415-d6ceddabc476.json'), scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('ECO2 Levels')

    # get the first sheet of the Spreadsheet
    try:
        sheet_instance = sheet.get_worksheet_by_id(0)
        sheet.del_worksheet(sheet_instance)
    except:
        pass
    now = datetime.now()
    try:
        new_sheet_instance = sheet.add_worksheet(rows = 1000,cols = 100,title = "{}".format(now.strftime("%b %d %Y")))
        new_sheet_instance.append_row(["Time","CO2 level"])
    except gspread.exceptions.APIError:
        new_sheet_instance = sheet.get_worksheet(-1)

    return new_sheet_instance
