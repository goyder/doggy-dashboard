import yaml
import dogdash.gsheets
from typing import IO
from dataclasses import dataclass, asdict
from typing import Optional, Iterable
import pandas as pd

@dataclass
class SpreadsheetConfig:
    spreadsheet_id: str
    worksheet_name: str
    column_renamings: Optional[dict]
    column_typing: Optional[dict]
    datetime_column: Optional[str]
    datetime_format: Optional[str]
    date_override_column: Optional[str]
    time_override_column: Optional[str]
    binary_columns: Optional[Iterable[str]]


class SpreadsheetManagers:
    def __init__(self, google_credential_filepath: str, config_file: IO):
        self.raw_config = yaml.safe_load(config_file)
        self.configs = self._convert_config_objects(self.raw_config)
        self.google_credential_filepath = google_credential_filepath

    @staticmethod
    def _convert_config_objects(raw_config: dict) -> Iterable[SpreadsheetConfig]:
        configs = []
        for config in raw_config.get("spreadsheets", []):
            configs.append(
                SpreadsheetConfig(
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
        return configs

    def assemble_spreadsheets(self):
        self.dfs = []
        for config in self.configs:
            df = dogdash.gsheets.load_spreadsheet(
                config.spreadsheet_id,
                config.worksheet_name,
                self.google_credential_filepath,

            )
            df = dogdash.gsheets.clean_spreadsheet(
                df,
                **asdict(config)
            )
            self.dfs.append(df)
        self.df_total = pd.concat(self.dfs)
        self.df_total.sort_values("datetime", ascending=True, inplace=True)
        