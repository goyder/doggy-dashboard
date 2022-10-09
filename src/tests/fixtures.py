import pytest
import pandas as pd

@pytest.fixture
def test_df():
    return pd.DataFrame({
        "A": ["1", "2", "3"],
        "B": ["4", "5", "6"],
        "C": ["TRUE", "FALSE", "TRUE"],
        "datetime": [
            "18/09/2022 23:00:00",
            "19/09/2022 03:00:00",
            "19/09/2022 06:15:00"],
        "date_override": [
            "25/12/2022",
            None,
            None
        ],
        "time_override": [
            "00:00:00",
            None,
            "13:00:00"
        ]
    })


@pytest.fixture
def sample_config():
    return """
spreadsheets:
    - 
        spreadsheet_id: 12345abcde
        worksheet_name: worksheet1
        column_renamings:
            A: a
            B: b
            C: c
        column_typing:
            A: str
            B: str
        binary_columns:
            - C
        time_override_column: time_override
        date_override_column: date_override
        datetime_format: "%d/%m/%Y %H:%M:%S"
    -
        spreadsheet_id: 678910fghij
        worksheet_name: worksheet2
    """
