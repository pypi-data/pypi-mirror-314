import boto3
import json
import os
from typing import List
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError


def get_glue_table_fields(
    glue: BaseClient, glue_prefix: str, database: str, table: str
) -> List[str]:
    glue_db = f"{glue_prefix}_{database}"
    try:
        response = glue.get_table(DatabaseName=glue_db, Name=table)
        if response.get("Table"):
            fields = [
                item["Name"]
                for item in response["Table"]["StorageDescriptor"]["Columns"]
            ]
        else:
            print("Table empty")
    except (ClientError, NoCredentialsError) as e:
        print(e)
        raise

    return fields


def handler(event, context):
    glue = boto3.client("glue")

    try:
        database = event["queryStringParameters"]["database"]
    except (TypeError, KeyError):
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": "Parameter `database` not specified",
        }
    try:
        table = event["queryStringParameters"]["table"]
    except (TypeError, KeyError):
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": "Parameter `table` not specified",
        }
    glue_prefix = os.environ.get("glue_prefix", None)

    table_fields = get_glue_table_fields(
        glue=glue, glue_prefix=glue_prefix, database=database, table=table
    )

    # Return API response json
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"table_fields": table_fields}),
    }
