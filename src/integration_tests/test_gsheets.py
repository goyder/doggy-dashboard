import pytest
import os
import dogdash.gsheets as gsheets
import pandas as pd

GOOGLE_SPREADSHEET_ID = os.environ["GOOGLE_SPREADSHEET_ID"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


sheet_names = os.environ.get("TARGET_SHEET_NAMES", "").replace("_", " ").split(",")


@pytest.mark.parametrize("sheet_name", sheet_names)
def test_sheet_retrieval(sheet_name: str):
    if sheet_name == "":
        pytest.skip()

    df = gsheets.load_spreadsheet(
        spreadsheet_id=GOOGLE_SPREADSHEET_ID,
        worksheet_name=sheet_name,
        service_credentials=GOOGLE_APPLICATION_CREDENTIALS
    )
    assert type(df) == pd.DataFrame