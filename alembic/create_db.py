from dogdash.connections import get_secret
import mysql.connector
import os

secret_name = os.environ["DB_CREDENTIALS_SECRET"]
region_name = os.environ["REGION"]
database_name = os.environ["DATABASE_NAME"]

secret = get_secret(secret_name, region_name)
cnx = mysql.connector.connect(
    user=secret["username"],
    password=secret["password"],
    host=secret["host"],
)
with cnx.cursor() as cur:
    # Check for existence of DB
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))