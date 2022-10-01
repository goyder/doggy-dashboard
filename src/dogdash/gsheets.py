import google.auth
from googleapiclient.discovery import build
import os
from googleapiclient.errors import HttpError
import gspread as gs
import pandas as pd

def load_spreadsheet(
    spreadsheet_id: str, 
    worksheet_name: str, 
    service_credentials=os.environ["GOOGLE_APPLICATION_CREDENTIALS"]) -> pd.DataFrame:
    """
    Pull a spreadsheet from Google sheets and return as a Pandas DataFrame.
    """
    gc = gs.service_account(filename=service_credentials)
    sh = gc.open_by_key(spreadsheet_id)
    ws = sh.worksheet(worksheet_name)
    df = pd.DataFrame(ws.get_all_records())
    return df