import boto3
import base64
from sqlalchemy import create_engine
from botocore.exceptions import ClientError
import json
import os
import tempfile


secret_name = os.environ["DB_CREDENTIALS_SECRET"]
region_name = os.environ["REGION"]
database_name = os.environ["DATABASE_NAME"]


def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            secret = json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            
    return secret


def secret_to_file(secret_name, region_name) -> str:
    secret = get_secret(secret_name, region_name)
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        json.dump(secret, f)
        credentials_filepath = f.name
    return credentials_filepath


def create_sqlalchemy_engine(
    database_name=database_name, 
    secret_name=secret_name, 
    region_name=region_name):
    secret = get_secret(
        secret_name=secret_name, 
        region_name=region_name
    )
    url = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}".format(
        DB_USER=secret["username"],
        DB_PASS=secret["password"],
        DB_HOST=secret["host"],
        DB_NAME=database_name
    )
    engine = create_engine(url=url)
    return engine