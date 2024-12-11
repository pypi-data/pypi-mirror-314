import json
import os
from typing import List

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError


def get_s3_objects(client: BaseClient, bucket: str, prefix: str) -> List[str]:
    """Get list of all objects in an S3 bucket (get keys).

    Parameters
    ----------
    client : S3
        Boto3 s3 client initialized with boto3.client("s3")
    bucket : str
        Name of the bucket to get objects from.
    prefix : str
        Subfolder of the bucket to get objects from.

    Returns
    -------
    List[str]
        List of S3 object keys.
    """
    bucket_objects = []
    continuation_token = None

    try:
        while True:
            if continuation_token:
                response = client.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
            else:
                response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)

            if "Contents" in response:
                for item in response["Contents"]:
                    bucket_objects.append(item["Key"])

                # Check if there are more pages
                if response.get("IsTruncated"):  # True if there are more pages
                    continuation_token = response["NextContinuationToken"]
                else:
                    break  # No more pages, exit loop
            else:
                print("Bucket empty or no objects with the specified prefix.")
                break
    except (ClientError, NoCredentialsError) as e:
        print(e)
        raise

    return bucket_objects


def get_table_names(s3_objects: List[str], database_name: str) -> List[str]:
    """Get table names for a specific database in the S3 object list
    Parameters
    ----------
    s3_objects : list
        List of keys of objects in the bucket.
    database_name : str
        Name of the database to list tables from.
    Returns
    -------
    List
        Sorted list of table names.
    """
    # Get all the bucket objects
    tables = set()
    for bucket_object in s3_objects:
        # Get table name for all objects with matching database name
        try:
            if (
                f"database={database_name}" in bucket_object
                or f"database_name={database_name}" in bucket_object
            ):
                components = bucket_object.split("/")
                table_name = [
                    item.split("=")[1]
                    for item in components
                    if item.startswith("table")
                ][0]
                print(table_name)
                tables.add(table_name)
        except IndexError:
            print(f"Could not split database and table name from {bucket_object}")
            continue
    return sorted(list(tables))


def handler(event, context):
    s3 = boto3.client("s3")

    # Fetch bucket_name and file_name using proxy integration method from API Gateway
    bucket = os.environ["bucket_name"]
    prefix = os.environ["prefix"]

    # Get list of objects from bucket
    s3_objects = get_s3_objects(s3, bucket, prefix)

    # Try to get database name from the API request
    try:
        database_name = event["queryStringParameters"]["databasename"]
    except TypeError:  # will try None["databasename"] if no databasename provided
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": "No database name specified",
        }

    # Work out the table names from the list of objects
    table_names = get_table_names(s3_objects, database_name.strip())

    # Return API response json
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"tables": table_names}),
    }
