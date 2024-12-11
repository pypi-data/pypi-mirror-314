"""
These lambda is used to check if a presigned URL has been requested and has subsequently been used in the past hour
in the  Uploader Service
"""
from abc import ABC, abstractmethod
import boto3
import os
import datetime
import time
import json
import logging
from urllib3 import PoolManager

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger()


class GetUnpackedLog(ABC):
    def __init__(self, log_group_name: str) -> None:
        self.log_group_name = log_group_name

    def get_logs(self) -> list:
        client = boto3.client("logs")
        query = 'fields @timestamp, @message| filter @message like "email: " or @message like "s3 key: " | sort @timestamp desc'

        start_query_response = client.start_query(
            logGroupName=self.log_group_name,
            startTime=int(
                (datetime.datetime.today() - datetime.timedelta(hours=1)).timestamp()
            ),
            endTime=int(datetime.datetime.now().timestamp()),
            queryString=query,
        )

        response = None
        while response is None or response["status"] == "Running":
            time.sleep(1)
            response = client.get_query_results(queryId=start_query_response["queryId"])

        logger.info(
            f"the following query has been executed on CloudWatch '{query}'. "
            f"The query was run on this log group: '{self.log_group_name}'"
        )

        return response["results"]

    @abstractmethod
    def unpack_log(self) -> None:
        raise NotImplementedError()


class UnpackUploadLog(GetUnpackedLog):
    def __init__(self, upload_log_group: str) -> None:
        super().__init__(upload_log_group)

    def unpack_log(self) -> dict:
        """
        The output of this method has the following structure:
        {
            "some@email.address": ["file name and metadata"],
            "some@email.address2": ["file name and metadata"]
        }
        """
        unpacked_values = {}
        file = None
        email = None
        for log_message in self.get_logs():
            logger.info(f"unpacking the following log: {log_message}")
            for inner in log_message:
                if inner["field"] == "@message":
                    if inner["value"].startswith("INFO:root:s3 key:"):
                        key = inner["value"]
                        file = key.split(" ")[2].split("\n")[0]
                    elif inner["value"].startswith("INFO:root:email:"):
                        value = inner["value"]
                        email = value.split(" ")[1].split("\n")[0]
            if file and email is not None:
                # Creates a dictionary with its value as a list
                unpacked_values.setdefault(email, []).append(file)
                file = None
                email = None

        logger.info("values for upload function are unpacked")
        return unpacked_values


class UnpackValidateLog(GetUnpackedLog):
    def __init__(self, validate_log_group: str) -> None:
        super().__init__(validate_log_group)

    def unpack_log(self) -> list:
        """
        The output of this method has the following structure:
        [
        "file1_path_name", "file2_path_name"
        ]
        """
        files = []
        for log_message in self.get_logs():
            logger.info(f"unpacking the following log: {log_message}")
            for inner in log_message:
                if inner["field"] == "@message":
                    if inner["value"].startswith("INFO:root:s3 key:"):
                        key = inner["value"]
                        file = key.split(" ")[2].split("\n")[0]
                        if file not in files:
                            files.append(key.split(" ")[2].split("\n")[0])

        logger.info("values for validate function are unpacked")
        return files


class EvaluateUnpackedLogs(object):
    def __init__(
        self, unpacked_upload_function: dict, unpacked_validate_function: list
    ) -> None:
        self.upload_logs = unpacked_upload_function
        self.validate_logs = unpacked_validate_function

    @staticmethod
    def send_slack_alert(email: str, file: str) -> None:
        try:
            http = PoolManager()
            url = os.getenv("WEBHOOK_URL")
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            now = now.replace("+00:00", "Z")
            payload = {
                "channel": os.getenv("CHANNEL"),
                "text": "Presigned URL not used",
                "username": "Uploader Service",
                "icon_emoji": ":lambda:",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"The user {email} created a presigned url for "
                            f"loading {file} and it has not been used in the last hour",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"*Event Source:* Unused Presigned URL \n"
                                f"*Event Time:* {now}"
                            ),
                        },
                    },
                ],
            }
            encoded_payload = json.dumps(payload).encode("utf-8")
            response = http.request(method="POST", url=url, body=encoded_payload)
            logger.info(
                {
                    "message": payload,
                    "status_code": response.status,
                    "response": response.data,
                }
            )
            return
        except Exception as e:
            logger.error(f"Failed to send an alert to Slack: {e}")

    def _check_if_loaded(self) -> dict:
        failed_loads = {}
        for email, value in self.upload_logs.items():
            for file in value:
                if file not in self.validate_logs:
                    failed_loads.setdefault(email, []).append(file)
        return failed_loads

    def handle(self) -> None:
        unused_presigned_urls = self._check_if_loaded()
        logger.info("checks for failed uploads performed")

        if bool(unused_presigned_urls):
            logger.info(f"failed uploaded: {unused_presigned_urls}")
            for email, files in unused_presigned_urls.items():
                if files:
                    for file in files:
                        self.send_slack_alert(email, file)

        else:
            logger.info("All requested presigned URLs have been used.")
            return
        return


def lambda_handler(event, context) -> None:
    # Get logs
    upload_function_logs = UnpackUploadLog(
        "/aws/lambda/ap-uploader-prod-upload-function-8c7a314"
    )
    if not upload_function_logs.get_logs():
        logger.info("no presigned urls have been requested in the last hour")
        return
    validate_function_logs = UnpackValidateLog(
        "/aws/lambda/data-eng-uploader-prod-validate"
    )

    # Unpack logs
    unpacked_upload_logs = upload_function_logs.unpack_log()
    unpacked_validate_logs = validate_function_logs.unpack_log()

    # Compare and send slack notification if needed
    EvaluateUnpackedLogs(unpacked_upload_logs, unpacked_validate_logs).handle()
