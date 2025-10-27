import os
import json
import boto3
import pandas as pd
from ftplib import FTP
import logging
import time
import sys

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
DATA_CONTRACT_PATH = os.environ.get("DATA_CONTRACT_PATH", "data_contract.json")
ATHENA_DATABASE = os.environ.get("ATHENA_DATABASE", "mealdash_lnd")
ATHENA_TABLE = os.environ.get("ATHENA_TABLE", "orders")
ATHENA_OUTPUT_S3 = os.environ.get("ATHENA_OUTPUT_S3", "s3://my-athena-query-results/")

# Load data contract
if not os.path.exists(DATA_CONTRACT_PATH):
    raise FileNotFoundError(f"Data contract file not found: {DATA_CONTRACT_PATH}")

with open(DATA_CONTRACT_PATH, "r") as f:
    contract = json.load(f)

conn_info = contract["connection_information"]
FTP_HOST = conn_info["host"]
FTP_USERNAME = conn_info["username"]
FTP_PASSWORD_SECRET_NAME = conn_info.get("password_secret_name")
FTP_FILE_PATH = conn_info["file_path"]
S3_DEST_PATH = conn_info["s3_destination"]

# Extract schema from contract
table_schema = contract.get("data_schema")
if not table_schema:
    raise ValueError("No 'data_schema' found in data_contract.json")

if not all([FTP_HOST, FTP_USERNAME, FTP_FILE_PATH, S3_DEST_PATH]):
    raise ValueError("Missing required connection info in data_contract.json")

# Fetch FTP password from Secrets Manager if specified
FTP_PASSWORD = None
if FTP_PASSWORD_SECRET_NAME:
    secrets_client = boto3.client("secretsmanager")
    secret_response = secrets_client.get_secret_value(SecretId=FTP_PASSWORD_SECRET_NAME)
    FTP_PASSWORD = secret_response.get("SecretString")
    if not FTP_PASSWORD:
        raise ValueError(f"No password found in secret {FTP_PASSWORD_SECRET_NAME}")

# Parse S3 bucket/key
if not S3_DEST_PATH.startswith("s3://"):
    raise ValueError("S3_DEST_PATH must start with s3://")
s3_parts = S3_DEST_PATH[5:].split("/", 1)
bucket_name = s3_parts[0]
prefix = s3_parts[1] if len(s3_parts) > 1 else ""
local_file = os.path.basename(FTP_FILE_PATH)

# AWS clients
s3_client = boto3.client("s3")
athena_client = boto3.client("athena")

# --------------------- FUNCTIONS ---------------------

def download_from_ftp():
    logger.info(f"Connecting to FTP {FTP_HOST}")
    with FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USERNAME, FTP_PASSWORD or "")
        logger.info(f"Downloading {FTP_FILE_PATH} to {local_file}")
        with open(local_file, "wb") as f:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH}", f.write)

def validate_schema():
    logger.info(f"Validating CSV {local_file} against schema from contract")
    df = pd.read_csv(local_file)
    errors = []

    for col_def in table_schema["orders"]:
        col_name = col_def["name"]
        col_type = col_def["datatype"]
        required = col_def.get("required", False)

        # Check required columns
        if required and col_name not in df.columns:
            errors.append(f"Required column '{col_name}' missing from CSV")
            continue  # Skip type check if column missing

        # Check data types if column exists
        if col_name in df.columns:
            try:
                if col_type in ["bigint", "integer"] and not pd.api.types.is_integer_dtype(df[col_name]):
                    errors.append(f"Column '{col_name}' is not integer type")
                elif col_type in ["double", "float"] and not pd.api.types.is_float_dtype(df[col_name]):
                    errors.append(f"Column '{col_name}' is not float/double type")
                elif col_type == "string" and not pd.api.types.is_string_dtype(df[col_name]):
                    errors.append(f"Column '{col_name}' is not string type")
            except Exception as e:
                errors.append(f"Column '{col_name}' type check error: {e}")

    if errors:
        for e in errors:
            logger.error(e)
        raise ValueError("Schema validation failed. See errors above.")
    else:
        logger.info("Schema validation passed.")

    return True

def upload_to_s3():
    s3_key = f"{prefix}/{local_file}" if prefix else local_file
    logger.info(f"Uploading {local_file} to s3://{bucket_name}/{prefix}")
    s3_client.upload_file(local_file, bucket_name, s3_key)
    logger.info("Upload complete")
    return f"s3://{bucket_name}/{s3_key}"

def load_to_athena(s3_path):
    columns_ddl = ",\n  ".join([f"{c['name']} {athena_type(c['datatype'])}" for c in table_schema["orders"]])
    ddl = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS {ATHENA_DATABASE}.{ATHENA_TABLE} (
      {columns_ddl}
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    WITH SERDEPROPERTIES ("separatorChar" = ",", "escapeChar" = "\\\\", "quoteChar" = "\\"")
    LOCATION '{s3_path.rsplit('/', 1)[0]}'
    TBLPROPERTIES ('has_encrypted_data'='false');
    """
    logger.info(f"Executing Athena DDL for table {ATHENA_DATABASE}.{ATHENA_TABLE}")
    response = athena_client.start_query_execution(
        QueryString=ddl,
        QueryExecutionContext={'Database': ATHENA_DATABASE},
        ResultConfiguration={'OutputLocation': ATHENA_OUTPUT_S3}
    )
    query_execution_id = response['QueryExecutionId']

    # Wait for query completion
    while True:
        status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(3)

    if state != 'SUCCEEDED':
        raise RuntimeError(f"Athena query failed with state {state}")
    logger.info("Data loaded into Athena successfully.")

def athena_type(json_type):
    mapping = {
        "bigint": "BIGINT",
        "integer": "INT",
        "double": "DOUBLE",
        "float": "FLOAT",
        "string": "STRING"
    }
    return mapping.get(json_type.lower(), "STRING")

# --------------------- MAIN EXECUTION ---------------------

if __name__ == "__main__":
    try:
        download_from_ftp()
        if validate_schema():
            s3_path = upload_to_s3()
            load_to_athena(s3_path)
    except Exception as e:
        logger.error(f"Batch job failed: {e}")
        sys.exit(1)

    logger.info("Batch job finished successfully.")
