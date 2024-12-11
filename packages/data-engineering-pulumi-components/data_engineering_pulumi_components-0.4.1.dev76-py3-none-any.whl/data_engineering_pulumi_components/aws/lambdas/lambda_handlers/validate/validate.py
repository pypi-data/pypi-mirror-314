import datetime
import fnmatch
import json
import logging
import os
from urllib.parse import unquote_plus
import functools
from typing import Callable

import boto3
from urllib3 import PoolManager

client = boto3.client("s3")

logging.basicConfig(level=logging.INFO, force=True)
root_logger = logging.getLogger()


def validate_object(func: Callable) -> Callable:
    """
    This simple function will just check to see if the key in the bucket exists,
    before executing the func
    """

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        source_bucket = kwargs["source_bucket"]
        source_key = kwargs["source_key"]

        s3 = boto3.client("s3")
        response = s3.list_objects_v2(Bucket=source_bucket)
        try:
            response["Contents"]
        except KeyError:
            root_logger.info(f"Bucket {source_bucket} is empty")
            raise

        keys = [key_info["Key"] for key_info in response["Contents"]]
        if source_key not in keys:
            root_logger.info(
                f"The file {source_key} does not exist in bucket {source_bucket}"
            )
        return func(*args, **kwargs)

    return wrapper_decorator


def validate_folder_structure(key: str):
    """The function will validate the folder structure (prefix) of S3 objects in the
    landing bucket to ensure they conform to the structure required by downstream
    processes.
    Parameters
    ----------
    key : str
        The S3 object key.
    """
    valid_prefixes = [
        "data/database_name=*_*/table_name=*/extraction_timestamp=*",
        "logs/database_name=*/table_name=*/extraction_timestamp=*",
        "metadata/database_name=*/table_name=db_and_table_list/extraction_timestamp=*",
    ]
    for prefix in valid_prefixes:
        if fnmatch.fnmatch(key, prefix):
            return True


@validate_object
def move_object(source_bucket: str, source_key: str, destination_bucket: str):
    """The function will copy the object in S3 to the "destination_bucket" bucket,
    while adding a timestamp to the filename. It will then
    delete the original object from "source_bucket".
    Parameters
    ----------
    destination_bucket : str
        The bucket where the S3 object will be copied to.
    source_bucket : str
        The bucket where the S3 object is.
    source_key : str
        The object S3 key.
    """
    client = boto3.client("s3")

    client.copy_object(
        Bucket=destination_bucket,
        CopySource={"Bucket": source_bucket, "Key": source_key},
        Key=source_key,
        ServerSideEncryption="AES256",
        ACL="bucket-owner-full-control",
    )
    client.delete_object(Bucket=source_bucket, Key=source_key)


def send_alert_to_slack(title, desc, event_source, source_id, msg, user, icon):
    """Sends an alert to Slack
    Parameters
    ----------
    title : str
        Event title
    desc : str
        Event description
    event_source : str
        Event source
    source_id : str
        Event source ID
    msg : str
        Message
    user : str
        Name of AWS service raising alerts
    icon : str
        Slack icon representing the service
    """
    try:
        http = PoolManager()
        url = os.getenv("WEBHOOK_URL")
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        now = now.replace("+00:00", "Z")
        payload = {
            "channel": os.getenv("CHANNEL"),
            "text": title,
            "username": user,
            "icon_emoji": icon,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{title} – {desc}",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*Event Source:* {event_source}\n"
                            f"*Event Time:* {now}\n"
                            f"*Source ID:* {source_id}\n"
                            f"*Message:* {msg}"
                        ),
                    },
                },
            ],
        }
        encoded_payload = json.dumps(payload).encode("utf-8")
        response = http.request(method="POST", url=url, body=encoded_payload)
        root_logger.info(
            {
                "message": payload,
                "status_code": response.status,
                "response": response.data,
            }
        )
    except Exception as e:
        root_logger.error(f"Failed to send an alert to Slack: {e}")


class EmptyFileError(Exception):
    """Raised when the file opened has no contents"""

    pass


class FileValidator:
    """
    A class to validate data in the Land-to-History pipeline. Currently
    merely checks that the file can be opened, and contains a non-zero
    amount of bytestream content. If both conditions are met, it moves
    to the pass bucket, otherwise moves the object to the fail bucket.
    Attributes
    ----------
    key : str
        The AWS S3 key of the file being validated.
    pass_bucket : str
        The name of the bucket for files that pass validation.
    fail_bucket : str
        The name of the bucket for files that fail validation.
    source_bucket : str
        The name of the bucket that contains the file being validated.
    """

    def __init__(
        self,
        key: str,
        size: int,
        pass_bucket: str,
        fail_bucket: str,
        source_bucket: str,
    ):
        """
        Parameters
        ----------
        key : str
            The AWS S3 key of the file being validated.
        size : int
            The size of the file being validated.
        pass_bucket : str
            The name of the bucket for files that pass validation.
        fail_bucket : str
            The name of the bucket for files that fail validation.
        source_bucket : str
            The name of the bucket that contains the file being validated.
        """
        self.key = key
        self.size = size
        self.fail_bucket = fail_bucket
        self.pass_bucket = pass_bucket
        self.source_bucket = source_bucket
        self.errors = []

    def _add_error(self, error: str):
        """Collects and aggregates error messges into a list.
        Parameters
        ----------
        error : str
            An error message
        """
        if error not in self.errors:
            self.errors.append(error)

    def _validate_file(self, key, size):
        """
        Parameters
        ----------
        key : str
            The AWS S3 key of the file being validated.
        size : int
            The size of the file being validated.
        """
        if validate_folder_structure(self.key) is not True:
            self._add_error(error=f"'{self.key}' Folder structure is invalid")
        elif self.size < 1:
            self._add_error(error=f"'{self.key}' File has no content")
            root_logger.error(self.key, self.size)

    def execute(self):
        self._validate_file(self.key, self.size)
        if len(self.errors) > 0:
            error = ", ".join(map(str, self.errors))
            move_object(
                destination_bucket=self.fail_bucket,
                source_bucket=self.source_bucket,
                source_key=self.key,
            )
            send_alert_to_slack(
                title="File validation",
                desc="Validation failure",
                event_source=f"Fail bucket {self.fail_bucket}",
                source_id=f"Source bucket {self.source_bucket}",
                msg=f"File {self.key} failed validation, Error - {error}",
                user="AWS Lambda",
                icon=":lambda:",
            )
            return {"validation_outcome": "Fail"}
        else:
            move_object(
                source_bucket=self.source_bucket,
                source_key=self.key,
                destination_bucket=self.pass_bucket,
            )
            return {"validation_outcome": "Pass"}


def handler(event, context):
    def log_status(
        validator_dict: dict, source_bucket: str, key: str, size: str
    ) -> None:
        root_logger.info(f"s3 source: {source_bucket}")
        root_logger.info(f"s3 key: {key}")
        root_logger.info(f"file size: {size}")
        root_logger.info(f"validation status: {validator_dict['validation_outcome']}")

    if event.get("scheduled_event"):
        source_bucket = os.environ["SOURCE_BUCKET"]
        bucket_objects = client.list_objects_v2(Bucket=source_bucket)
        if bucket_objects["KeyCount"] > 0:
            paginator = client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=source_bucket)
            for page in pages:
                for obj in page["Contents"]:
                    pass_bucket = os.environ["PASS_BUCKET"]
                    fail_bucket = os.environ["FAIL_BUCKET"]
                    key = obj["Key"]
                    size = obj["Size"]
                    fileValidator = FileValidator(
                        key=key,
                        size=size,
                        pass_bucket=pass_bucket,
                        fail_bucket=fail_bucket,
                        source_bucket=source_bucket,
                    )
                    root_logger.info(f"s3 key: {key}")
                    val_dict = fileValidator.execute()
                    log_status(val_dict, source_bucket, key, size)

    elif event.get("Records"):
        for record in event["Records"]:
            source_bucket = record["s3"]["bucket"]["name"]
            pass_bucket = os.environ["PASS_BUCKET"]
            fail_bucket = os.environ["FAIL_BUCKET"]
            key = unquote_plus(record["s3"]["object"]["key"])
            size = record["s3"]["object"]["size"]
            fileValidator = FileValidator(
                key=key,
                size=size,
                pass_bucket=pass_bucket,
                fail_bucket=fail_bucket,
                source_bucket=source_bucket,
            )
            root_logger.info(f"s3 key: {key}")
            val_dict = fileValidator.execute()
            log_status(val_dict, source_bucket, key, size)

    else:
        raise KeyError
