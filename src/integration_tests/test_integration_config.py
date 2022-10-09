import dogdash.config 
import pytest
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
required_columns = ["datetime", "pee", "poo", "accident"]

def test_configuration_execution():
    config_file_name = "integration_config.yaml"
    config_file_path = os.path.join(dir_path, config_file_name)
    if not os.path.exists(config_file_path):
        pytest.skip("No config file provided.")
    credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    with open(config_file_path, 'r') as f:
        spreadsheet_manager = dogdash.config.SpreadsheetManagers(credentials, f)
    spreadsheet_manager.assemble_spreadsheets()

    df = spreadsheet_manager.df_total

    assert all([column_name in df.columns for column_name in required_columns])
    assert df.datetime.is_monotonic_increasing
