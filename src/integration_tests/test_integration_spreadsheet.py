import dogdash.spreadsheet 
import dogdash.connections
import pytest
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
required_columns = ["datetime", "pee", "poo", "accident"]
config_file_name = "integration_config.yaml"
config_file_path = os.path.join(dir_path, config_file_name)


def test_configuration_execution():
    if not os.path.exists(config_file_path):
        pytest.skip("No config file provided.")

    credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    config = dogdash.spreadsheet.Configuration.from_yaml_file(config_file_path)
    spreadsheet = dogdash.spreadsheet.Spreadsheet(credentials, config=config)
    spreadsheet.assemble_spreadsheets()

    df = spreadsheet.df_total

    assert all([column_name in df.columns for column_name in required_columns])
    assert df.datetime.is_monotonic_increasing


def test_configuration_execution_from_parameter_store():
    parameter_store_path = os.environ.get("INTEGRATION_TEST_PARAMETER_STORE_CONFIG_PATH", None)
    if not parameter_store_path:
        pytest.skip("No parameter path available.")

    credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    config = dogdash.spreadsheet.Configuration.from_parameter_store(parameter_store_path)
    spreadsheet = dogdash.spreadsheet.Spreadsheet(credentials, config=config)
    spreadsheet.assemble_spreadsheets()

    df = spreadsheet.df_total

    assert all([column_name in df.columns for column_name in required_columns])
    assert df.datetime.is_monotonic_increasing


def test_write_to_sql_database():
    if not os.path.exists(config_file_path):
        pytest.skip("No config file provided.")

    credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    config = dogdash.spreadsheet.Configuration.from_yaml_file(config_file_path)
    sql_engine = dogdash.connections.create_sqlalchemy_engine()

    spreadsheet = dogdash.spreadsheet.Spreadsheet(credentials, config=config)
    spreadsheet.assemble_spreadsheets()
    spreadsheet.write_to_sql(
        "integration_dev_table",
        sql_engine,
        if_exists="replace"
    )
    
