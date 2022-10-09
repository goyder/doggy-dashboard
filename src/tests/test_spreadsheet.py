from random import sample
import dogdash.gsheets
import dogdash.spreadsheet
import pandas as pd
from tests.fixtures import test_df, sample_config
from pytest_mock.plugin import MockerFixture
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
config_file_name = "test_config.yaml"
config_file_path = os.path.join(dir_path, config_file_name)


def test_config_read_from_text(sample_config):
    # Pass in our config
    config = dogdash.spreadsheet.Configuration.from_text(sample_config)

    assert config.raw_config["spreadsheets"][0]["spreadsheet_id"] == "12345abcde"
    assert config.spreadsheet_configs[0].spreadsheet_id == "12345abcde"
    assert config.spreadsheet_configs[1].spreadsheet_id == "678910fghij"


def test_config_read_from_file():
    # Pass in our config
    config = dogdash.spreadsheet.Configuration.from_yaml_file(config_file_path)

    assert config.raw_config["spreadsheets"][0]["spreadsheet_id"] == "12345abcde"
    assert config.spreadsheet_configs[0].spreadsheet_id == "12345abcde"
    assert config.spreadsheet_configs[1].spreadsheet_id == "678910fghij"


def test_config_read_from_parameter_store(mocker: MockerFixture, sample_config):
    mocked_parameter_store_retrieval = mocker.patch(
        "dogdash.spreadsheet.ssm_client.get_parameter",
        return_value={
            "Parameter": {
                "Name": "parameter_name",
                "Value": sample_config
            }
        }
    )
    
    config = dogdash.spreadsheet.Configuration.from_parameter_store("/sample/configuration_location")

    assert config.raw_config["spreadsheets"][0]["spreadsheet_id"] == "12345abcde"
    assert config.spreadsheet_configs[0].spreadsheet_id == "12345abcde"
    assert config.spreadsheet_configs[1].spreadsheet_id == "678910fghij"


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
    config = dogdash.spreadsheet.Configuration.from_text(sample_config)
    spreadsheet = dogdash.spreadsheet.Spreadsheet(
        google_credential_filepath="nah",
        config=config
    )
    spreadsheet.assemble_spreadsheets()

    assert mocked_load_spreadsheet.call_args_list[0].args == ('12345abcde', 'worksheet1', "nah")
    assert mocked_load_spreadsheet.call_args_list[1].args == ('678910fghij', 'worksheet2', "nah")


def test_create_stream_from_config_file():
    config = dogdash.spreadsheet.Configuration.from_yaml_file(config_file_path)
