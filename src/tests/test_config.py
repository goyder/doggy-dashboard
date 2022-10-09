import dogdash.gsheets
import dogdash.config
import pandas as pd
from tests.fixtures import test_df, sample_config
from pytest_mock.plugin import MockerFixture


def test_config_read(sample_config):
    # Pass in our config
    spreadsheet_manager = dogdash.config.SpreadsheetManagers(
        google_credential_filepath="nah",
        config_file=sample_config
    )

    assert spreadsheet_manager.raw_config["spreadsheets"][0]["spreadsheet_id"] == "12345abcde"
    assert spreadsheet_manager.configs[0].spreadsheet_id == "12345abcde"
    assert spreadsheet_manager.configs[1].spreadsheet_id == "678910fghij"


def test_spreadsheet_call(mocker: MockerFixture, test_df, sample_config):
    # Define our mocks 
    mocked_load_spreadsheet = mocker.patch(
        "dogdash.gsheets.load_spreadsheet",
        return_value=test_df
    )
    mocked_clean_spreadsheet = mocker.patch(
        "dogdash.gsheets.clean_spreadsheet",
        return_value=test_df)

    # Pass in our config
    spreadsheet_manager = dogdash.config.SpreadsheetManagers(
        google_credential_filepath="nah",
        config_file=sample_config
    )
    spreadsheet_manager.assemble_spreadsheets()

    assert mocked_load_spreadsheet.call_args_list[0].args == ('12345abcde', 'worksheet1', "nah")
    assert mocked_load_spreadsheet.call_args_list[1].args == ('678910fghij', 'worksheet2', "nah")