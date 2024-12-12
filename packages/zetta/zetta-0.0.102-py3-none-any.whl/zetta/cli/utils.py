# Copyright ZettaBlock Labs 2024
import os

import boto3
import pyiceberg
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
import configparser
import requests

ICEBERG_DATA_LOCATION = "s3://ai-network-worker-demo/iceberg-data/"
S3_BUCKET = "ai-network-worker-demo"
S3_REGION = "us-east-1"
AWS_DATA_CATALOG = "AwsDataCatalog"
NEO_DEV_URL = "https://neo-dev.prod.zettablock.com/v1/api"
CREATE_DATASET_NEO_URL = "{}/dataset/create".format(NEO_DEV_URL)


def list_parquet_files(path_str):
    files = []
    for file in os.listdir(path_str):
        if file.endswith('.parquet'):
            files.append((os.path.join(path_str, file), file))
    return files


def upload_s3(parquet_file, bucket, key):
    """
    Args:
        :param parquet_file:
        :param bucket:
        :param key:
    """
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv("AWS_KEY_ID"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    s3.upload_file(parquet_file, bucket, key)
    return f's3://{bucket}/{key}'


def add_files_to_iceberg(table: pyiceberg.catalog.Table, parquet_file):
    table.add_files(parquet_file)


def create_iceberg_ns_and_table(ns: str = "ai-lake-test",
                                table_name: str = "imagenet-object-localization-challenge-nov26",
                                schema: Schema = None,
                                location: str = "s3://ai-network-worker-demo/iceberg-data/"):
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": S3_REGION,
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    catalog.create_namespace_if_not_exists(ns)

    # Create an Iceberg table
    table = catalog.create_table_if_not_exists(
        identifier="{}.{}".format(ns, table_name),
        schema=schema,
        location=location)
    return table


def list_iceberg_tables(ns: str = "ai-lake-test"):
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": S3_REGION,
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    tables = []
    for ns, tbl in catalog.list_tables(ns):
        tables.append('{}.{}'.format(ns, tbl))
    return tables


def list_iceberg_table(ns: str = "ai-lake-test", table: str = ""):
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": S3_REGION,
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    return catalog.load_table("{}.{}".format(ns, table)).schema()


def get_catalog():
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": S3_REGION,
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    return catalog


def register_datasets_v2_to_neo(j):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        # token = config.get('default', 'token', fallback=None)
        api_key = config.get('default', 'api_key', fallback=None)
        user = config.get('default', 'user_name', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")

    j['user'] = user

    headers = {
        # "Authorization": token,
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
    }

    json_data = j

    print('posting to neo: {}'.format(j))

    response = requests.post(CREATE_DATASET_NEO_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        print(f'Successfully created dataset {response.json()}')
    else:
        response.raise_for_status()


def list_datasets_v2_from_neo(dataset_id: str):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        api_key = config.get('default', 'api_key', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
    }
    if dataset_id:
        url = "{}/dataset/get?id={}".format(NEO_DEV_URL, dataset_id)
    else:
        url = "{}/dataset/list".format(NEO_DEV_URL)
    response = requests.request("GET", url, headers=headers)

    print(response.text)


def list_databases_v2_from_neo():
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        api_key = config.get('default', 'api_key', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
    }

    url = "{}/database/list".format(NEO_DEV_URL)
    response = requests.request("GET", url, headers=headers)

    print(response.text)


def get_database_v2_from_neo(name):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        api_key = config.get('default', 'api_key', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key,
    }

    url = "{}/database/get?name={}".format(NEO_DEV_URL, name)
    response = requests.request("GET", url, headers=headers)

    print(response.text)

