import google.auth
from googleapiclient.discovery import build
import os
from googleapiclient.errors import HttpError
import gspread as gs
import pandas as pd
from typing import Optional
import numpy as np


def load_spreadsheet(
    spreadsheet_id: str, 
    worksheet_name: str, 
    service_credentials: str) -> pd.DataFrame:
    """
    Pull a spreadsheet from Google sheets and return as a Pandas DataFrame.
    """
    gc = gs.service_account(filename=service_credentials)
    sh = gc.open_by_key(spreadsheet_id)
    ws = sh.worksheet(worksheet_name)
    df = pd.DataFrame(ws.get_all_records())
    return df


def clean_spreadsheet(
    df: pd.DataFrame,
    column_renamings: Optional[dict] = None,
    column_typing: Optional[dict] = None,
    datetime_column: Optional[str] = None,
    datetime_format: Optional[str] = None,
    date_override_column: Optional[str] = None,
    time_override_column: Optional[str] = None
) -> pd.DataFrame:
    """
    Rename columns, handle datetimes.
    """
    if column_renamings:
        df = df.rename(columns=column_renamings)

    if column_typing:
        df = df.astype(dtype=column_typing)
    
    if datetime_column:
        df[datetime_column] = pd.to_datetime(
            df[datetime_column], 
            format=datetime_format
            )

    if date_override_column:
        df[date_override_column] = (
            pd.to_datetime(
                np.where(
                    df[date_override_column].isna(), 
                    df[datetime_column].dt.date,
                    df[date_override_column])
            )
        )
        df[datetime_column] = pd.to_datetime(
            df[date_override_column].dt.date.astype(str) + " " + df[datetime_column].dt.time.astype(str)
        )

    if time_override_column:
        df[time_override_column] = (
            np.where(
                df[time_override_column].isna(), 
                df[datetime_column].dt.time,
                df[time_override_column])
        )
        df[datetime_column] = pd.to_datetime(
            df[datetime_column].dt.date.astype(str) + " " + df[time_override_column].astype(str)
        )

    return df