import yaml
import dogdash.gsheets
from typing import IO
from dataclasses import dataclass, asdict
from typing import Optional, Iterable
import pandas as pd
import boto3

ssm_client = boto3.client("ssm")


@dataclass
class GooglesheetsSpreadsheetConfig:
    spreadsheet_id: str
    worksheet_name: str
    column_renamings: Optional[dict]
    column_typing: Optional[dict]
    datetime_column: Optional[str]
    datetime_format: Optional[str]
    date_override_column: Optional[str]
    time_override_column: Optional[str]
    binary_columns: Optional[Iterable[str]]


class Configuration:
    def __init__(self, raw_config):
        self.raw_config = raw_config
        self._convert_config_objects(raw_config)

    @classmethod
    def from_text(cls, raw_config_string: str):
        raw_config = yaml.safe_load(raw_config_string)
        return cls(raw_config)

    @classmethod
    def from_yaml_file(cls, yaml_file_path: str): 
        with open(yaml_file_path, 'r') as f:
            raw_config = yaml.safe_load(f)
        return cls(raw_config)

    @classmethod
    def from_parameter_store(cls, parameter_name: str):
        response = ssm_client.get_parameter(
            Name=parameter_name
        )
        raw_config_string = response["Parameter"]["Value"]
        raw_config = yaml.safe_load(raw_config_string)
        return cls(raw_config)

    def _convert_config_objects(self, raw_config: dict):
        configs = []
        for config in raw_config.get("spreadsheets", []):
            configs.append(
                GooglesheetsSpreadsheetConfig(
                    spreadsheet_id=config.get("spreadsheet_id", None),
                    worksheet_name=config.get("worksheet_name", None),
                    column_renamings=config.get("column_renamings", None),
                    column_typing=config.get("column_typing", None),
                    datetime_column=config.get("datetime_column", None),
                    datetime_format=config.get("datetime_format", None),
                    date_override_column=config.get("date_override_column", None),
                    time_override_column=config.get("time_override_column", None),
                    binary_columns=config.get("binary_columns", None)
                )
            )
        self.spreadsheet_configs = configs
        

class Spreadsheet:
    def __init__(self, google_credential_filepath: str, config: Configuration):
        self.config = config
        self.google_credential_filepath = google_credential_filepath

    def assemble_spreadsheets(self):
        self.dfs = []
        for spreadsheet_config in self.config.spreadsheet_configs:
            df = dogdash.gsheets.load_spreadsheet(
                spreadsheet_config.spreadsheet_id,
                spreadsheet_config.worksheet_name,
                self.google_credential_filepath,
            )
            df = dogdash.gsheets.clean_spreadsheet(
                df,
                **asdict(spreadsheet_config)
            )
            self.dfs.append(df)
        self.df_total = pd.concat(self.dfs)
        self.df_total.sort_values("datetime", ascending=True, inplace=True)
        