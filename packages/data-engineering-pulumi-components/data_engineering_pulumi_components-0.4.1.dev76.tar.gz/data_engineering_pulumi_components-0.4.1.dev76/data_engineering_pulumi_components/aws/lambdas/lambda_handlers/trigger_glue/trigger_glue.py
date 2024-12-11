import boto3
import os


def handler(event, context):
    print(event)

    sts_connection = boto3.client("sts")
    ap_account = sts_connection.assume_role(
        RoleArn=os.environ["CROSS_ACCOUNT_ROLE"],
        RoleSessionName="trigger_glue_job_cross_account",
    )

    ACCESS_KEY = ap_account["Credentials"]["AccessKeyId"]
    SECRET_KEY = ap_account["Credentials"]["SecretAccessKey"]
    SESSION_TOKEN = ap_account["Credentials"]["SessionToken"]

    # create service client using the assumed role credentials
    glue = boto3.client(
        "glue",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
        region_name=os.environ["JOB_REGION"],
    )
    gluejobname = os.environ["GLUE_JOB_NAME"]

    try:
        runId = glue.start_job_run(
            JobName=gluejobname, Arguments={"--key": event["object"]["key"]}
        )

        status = glue.get_job_run(JobName=gluejobname, RunId=runId["JobRunId"])
        print("Job Status : ", status["JobRun"]["JobRunState"])

    except Exception as e:
        print(e)
