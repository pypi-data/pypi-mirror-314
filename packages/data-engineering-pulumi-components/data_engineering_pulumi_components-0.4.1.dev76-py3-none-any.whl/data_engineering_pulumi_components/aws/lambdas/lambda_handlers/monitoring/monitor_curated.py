import boto3
import os
import logging
from datetime import datetime, timezone
from urllib3 import PoolManager
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        logger.info(
            {
                "message": payload,
                "status_code": response.status,
                "response": response.data,
            }
        )
    except Exception as e:
        logger.error(f"Failed to send an alert to Slack: {e}")


def handler(event, context):

    source_bucket = os.getenv("SOURCE_BUCKET")
    pieline_name = os.getenv("PIPELINE_NAME")
    specified_time = int(os.getenv("SPECIFIED_TIME", "60"))

    s3_client = boto3.client("s3")

    try:
        current_time = datetime.now(timezone.utc)

        #  s3_client.list_objects_v2(Bucket="dbt-tables-sandbox", Prefix="sandbox/models")
        response = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=pieline_name)

        if "Contents" in response:
            files = response["Contents"]
            logger.info(f"Found {len(files)} file(s) in '{pieline_name}'")

            for file in files:
                file_key = file["Key"]
                last_modified = file["LastModified"]
                # TO DO - make sure to change data types to strings for f
                # string.
                # think about how specified time is passed in ...

                time_diff = (current_time - last_modified).total_seconds() / 60
                if time_diff <= specified_time:
                    logger.info(f"New file detected: {file_key}")
                else:
                    logger.info(
                        f"Latest file '{file_key}' is older than {specified_time} minutes."
                    )

                    send_alert_to_slack(
                        title="Freshness alert",
                        desc="No new file loaded",
                        event_source=f"{source_bucket}",
                        source_id=f"Source key {pieline_name}",
                        msg=f"No new file has moved to curated in {pieline_name} for {time_diff} minutes.",
                        user="AWS Lambda",
                        icon=":lambda:",
                    )
        else:
            logger.info(f"No files found in '{pieline_name}'")
    except Exception as e:
        logger.error(f"Error processing S3 bucket: {str(e)}")
