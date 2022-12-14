import dogdash.gsheets as gsheets
import pytest
import pandas as pd
from tests.fixtures import test_df

def test_rename_columns(test_df):
    column_renamings = {
        "A": "a",
        "B": "b",
        "C": "c"
    }   
    df = gsheets.clean_spreadsheet(
        test_df,
        column_renamings=column_renamings
    )   
    for original_column, new_column in column_renamings.items():
        assert original_column not in df.columns
        assert new_column in df.columns


def test_set_column_typing(test_df):
    column_typing = {
        "A": int,
        "B": int,
        "C": bool    
        }
    df = gsheets.clean_spreadsheet(
        test_df,
        column_typing=column_typing,
        datetime_column="datetime",
        datetime_format="%d/%m/%Y %H:%M:%S"
    )
    for column in column_typing:
        assert df[column].dtype == column_typing[column]

    assert pd.api.types.is_datetime64_any_dtype(df["datetime"])


def test_date_overriding(test_df):
    df = gsheets.clean_spreadsheet(
        test_df,
        datetime_column="datetime",
        datetime_format="%d/%m/%Y %H:%M:%S",
        date_override_column="date_override"
    )

    assert (df["datetime"].dt.date == [pd.to_datetime(date_str) for date_str in ["2022-12-25", "2022-09-19", "2022-09-19"]]).all()


def test_time_overriding(test_df):
    df = gsheets.clean_spreadsheet(
        test_df,
        datetime_column="datetime",
        datetime_format="%d/%m/%Y %H:%M:%S",
        time_override_column="time_override"
    )

    assert (df["datetime"].dt.time.astype(str) == ["00:00:00", "03:00:00", "13:00:00"]).all()


def test_date_and_time_overriding(test_df):
    df = gsheets.clean_spreadsheet(
        test_df,
        datetime_column="datetime",
        datetime_format="%d/%m/%Y %H:%M:%S",
        time_override_column="time_override",
        date_override_column="date_override"
    )

    assert (df["datetime"].dt.time.astype(str) == ["00:00:00", "03:00:00", "13:00:00"]).all()
    assert (df["datetime"].dt.date == [pd.to_datetime(date_str) for date_str in ["2022-12-25", "2022-09-19", "2022-09-19"]]).all()


def test_binary_transformation(test_df):
    df = gsheets.clean_spreadsheet(
        test_df,
        binary_columns=["C"],
    )

    assert (df["C"] == [True, False, True]).all()


def test_drop_columns(test_df):
    df = gsheets.clean_spreadsheet(
        test_df,
        columns_to_keep=["B", "C"]
    )
    assert set(df.columns.to_list()) == set(["B", "C"])