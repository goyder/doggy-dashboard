import dogdash.spreadsheet
import dogdash.connections
import os

credentials_secret_name = os.environ["GOOGLE_APPLICATION_CREDENTIALS_SECRET_NAME"]
region = os.environ["REGION"]
parameter_name = os.environ["PARAMETER_STORE_NAME"]
db_secret_name = os.environ["DB_SECRET_NAME"]
database_name = os.environ["DB_NAME"]
table_name = os.environ["DB_TABLE_NAME"]

config = dogdash.spreadsheet.Configuration.from_parameter_store(parameter_name)
sql_engine = dogdash.connections.create_sqlalchemy_engine(
    database_name=database_name,
    secret_name=db_secret_name,
    region_name=region
)
google_credentials_filepath = dogdash.connections.secret_to_file(
    credentials_secret_name,
    region
)

def handler(event, context):
    spreadsheet = dogdash.spreadsheet.Spreadsheet(
        google_credential_filepath=google_credentials_filepath,
        config=config
    )
    spreadsheet.assemble_spreadsheets()
    spreadsheet.write_to_sql(
        table_name=table_name,
        sql_engine=sql_engine,
        if_exists="replace"
    )