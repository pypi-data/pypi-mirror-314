from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
import sys
from awsglue.job import Job
from datetime import datetime as dt
import boto3
from string import Template
import json
import datetime
from urllib3 import PoolManager
import logging
import os

logging.basicConfig(level=logging.INFO)
root_logger = logging.getLogger()


class InvalidFileType(Exception):
    pass


def time_column_converter(dataframe: DataFrame, column: str, format: str):
    non_nulls = dataframe.agg(
        F.sum(F.when(F.col(column).isNotNull(), 1).otherwise(0))
    ).first()[0]
    if format == "iso":
        dataframe = dataframe.withColumn(column, F.split(column, r"\.").getItem(0))
        dataframe = dataframe.withColumn(
            column, F.to_timestamp(column, "yyyy-MM-dd'T'HH:mm:ss")
        )
    else:
        dataframe = dataframe.withColumn(column, F.to_timestamp(column, format))
    converted = dataframe.agg(
        F.sum(F.when(F.col(column).isNotNull(), 1).otherwise(0))
    ).first()[0]
    if non_nulls != converted:
        print(
            f"Warning! {column} had {non_nulls} timestamps, "
            + f"and now has {converted} non_null timestamps!"
        )
    print("converted column " + column)
    return dataframe


def date_finder(input: str):
    formats = [
        "%Y%m%d%H%M%SZ",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%y",
        "%d/%m/%Y",
    ]
    # mapping converts python dates to simple dates for java
    mapping = {
        "Y": "yyyy",
        "y": "yy",
        "m": "MM",
        "d": "dd",
        "dT": "dd'T'",
        "H": "HH",
        "M": "mm",
        "S": "ss",
        "SZ": "ss'Z'",
    }
    # TODO - Find more common formats from inspecting user data
    correct_format = None
    for format in formats:
        try:
            dt.strptime(input, format)
            correct_format = format
            break
        except ValueError:
            continue
    if correct_format is None:
        try:
            dt.fromisoformat(input)
            return_format = "iso"
        except ValueError:
            return_format = None
            pass
    else:
        return_format = Template(correct_format.replace("%", "$")).substitute(**mapping)
    return return_format


def date_converter(dataframe: DataFrame):
    try:
        sample = (
            dataframe.select(
                [F.first(x, ignorenulls=True).alias(x) for x in dataframe.columns]
            )
            .first()
            .asDict()
        )
    except Exception:
        print("dataframe of appears to have no rows!")
        return dataframe

    date_columns = {}
    for column in sample:
        # Only bother checking if it's already not a non-string type
        if type(sample[column]) == str:
            date_format = date_finder(sample[column])
            if date_format is not None:
                date_columns[column] = date_format

    for column in date_columns:
        dataframe = time_column_converter(
            dataframe=dataframe, column=column, format=date_columns[column]
        )
    return dataframe


def convert_struct_to_string(dataframe: DataFrame):
    """If a column with a struct data type is detected, convert it to
        a string"""
    for column_name, data_type in dataframe.dtypes:
        if 'struct' in data_type:
            dataframe = dataframe.withColumn(column_name, F.col(column_name).cast('string'))
    return dataframe


def replace_space_in_string(name: str) -> str:
    """
    If a string contains space inbetween, then replace by underscore.
    If it contains brackets then remove them.
    """
    replaced_name = name.strip().replace(" ", "_").replace("(", "").replace(")", "")
    return replaced_name


def dynamic_frame_to_glue_catalog(
    path: str,
    table_name: str,
    database_name: str,
    dynamic_frame: DynamicFrame,
    glue_context: GlueContext,
):
    """
    Adds a given Glue DynamicFrame to the Glue Catalog,
    by writing it out to the supplied path

    Arguments:
    path: str
        A S3 path of the format s3://path/to/file/
    table_name: str
        The desired name of the table
    database name: str
        The name of the database which the table is to appear in.
    dynamic_frame: DynamicFrame
        A Glue DynamicFrame, including partitioning info, to be written out.
    glue_context:
        An AWS GlueContext
    """
    print("Attempting to register to Glue Catalogue")
    try:
        sink = glue_context.getSink(
            connection_type="s3",
            path=path,
            enableUpdateCatalog=True,
            updateBehavior="UPDATE_IN_DATABASE",
            partitionKeys=["extraction_timestamp"],
        )

        sink.setFormat("glueparquet")
        sink.setCatalogInfo(catalogDatabase=database_name, catalogTableName=table_name)
        sink.writeFrame(dynamic_frame)
        print("Write out of file succeeded!")
    except Exception as e:
        print(f"Could not convert {path} to glue table, due to an error!")
        print(e)


def send_alert_to_slack(
    title, desc, event_source, source_id, msg, user, icon, args: dict
):
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
    args : dict
        args fed into script
    """
    try:
        http = PoolManager()
        url = args["webhook_url"]
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        now = now.replace("+00:00", "Z")
        payload = {
            "channel": args["channel"],
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


def files_to_dynamic_frame(
    path: str,
    filetype: str,
    source_bucket: str,
    table_name: str,
    allow_data_conversion: str,
    extraction_timestamp: str,
    spark: SparkSession,
    glue_context: GlueContext,
    args: dict,
    allow_struct_conversion: str = "False"
):
    """
    Reads in files at a filepath, and transforms them into
    a partitioned DynamicFrame using Spark and Glue.

    Arguments:
    path: str
        A S3 path of the format path/to/file/, not including any "s3://" prefixes
    filetype: str
        A filetype, currently only of the format "csv" or "json/jsonl"
    source_bucket: str
        The name of AWS bucket in which the files are contained.
    table_name: str
        The name of the table to be constructed.
    spark: SparkSession
        A SparkSession to be used to construct a Dataframe,
        containing the partitioned data.
    glue_context:
        An AWS GlueContext
    args: dict
        Dict of args fed to the script
    """
    try:
        file_location = "s3://" + source_bucket + "/" + path
        if filetype == "csv":
            datasource = spark.read.load(
                path=file_location,
                format="csv",
                header="true",
                multiLine=True,
                escape='"',
            )
        else:
            datasource = spark.read.load(
                path=file_location,
                format="json",
            )
        print(f"Successfully read files at {path} to Spark")

        # If the columnname contains space and add an underscore\
        datasource = datasource.withColumn(
            "extraction_timestamp", (F.lit(extraction_timestamp))
        )
        exprs = [
            F.col(column).alias(replace_space_in_string(column))
            for column in datasource.columns
        ]
        renamed_datasource = datasource.select(*exprs)
        print(f"Converting dates for {path}")

        # Set finalised = to renamed to account for conversions
        finalised_datasource = renamed_datasource

        if allow_data_conversion == "True":
            finalised_datasource = date_converter(finalised_datasource)

        if allow_struct_conversion == "True":
            finalised_datasource = convert_struct_to_string(finalised_datasource)

        dynamic_frame = DynamicFrame.fromDF(
            finalised_datasource, glue_context, table_name
        )

        return dynamic_frame

    except Exception as e:
        print(f"Could not convert {file_location} to dynamic_frame, due to an error!")
        send_alert_to_slack(
            title="Glue validation error",
            desc="Dynamic frame conversion error",
            event_source=f"Bucket {file_location}",
            source_id=f"Source table {table_name}",
            msg=e,
            user="AWS Lambda",
            icon=":lambda:",
            args=args,
        )
        print(e)
        raise e


def setup_glue(inputs: dict):
    """
    Setup glue environment and create a spark session

    Returns a spark session and glue context
    """
    sc = SparkContext()
    sc._jsc.hadoopConfiguration().set("fs.s3.canned.acl", "BucketOwnerFullControl")
    glueContext = GlueContext(sc)
    job = Job(glueContext)
    job.init(inputs["JOB_NAME"], inputs)
    glueContext._jsc.hadoopConfiguration().set(
        "fs.s3.enableServerSideEncryption", "true"
    )
    glueContext._jsc.hadoopConfiguration().set(
        "fs.s3.canned.acl", "BucketOwnerFullControl"
    )
    spark = glueContext.spark_session

    return spark, glueContext


def job_inputs():
    return getResolvedOptions(
        sys.argv,
        [
            "JOB_NAME",
            "source_bucket",
            "destination_bucket",
            "stack_name",
            "multiple_db_in_bucket",
            "allow_data_conversion",
            "allow_struct_conversion",
            "webhook_url",
            "channel",
            "project",
            "key",
        ],
    )


def list_of_data_objects_to_process(bucket, project):
    """
    List all objects under the raw_history/ path for a given project.
    Returns the full response from the list_object_v2 call.
    """
    client = boto3.client("s3")
    print("Listing Objects")
    paginator = client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(
        Bucket=bucket, Prefix=f"raw_history/{project}/data/"
    )
    response = []
    try:
        for page in page_iterator:
            response += page["Contents"]
    except KeyError as e:
        print(f"No {e} key found in bucket contents – either the bucket")
        print(" is empty or the data folder isn't available")

    return response


def does_database_exist(client, database_name):
    """Determine if this database exists in the Data Catalog
    The Glue client will raise an exception if it does not exist.
    """
    try:
        client.get_database(Name=database_name)
        return True
    except client.exceptions.EntityNotFoundException:
        return False


def print_inputs(inputs: dict):
    print(
        f"Job name: {args['JOB_NAME']},",
        f"source_bucket: {args['source_bucket']},",
        f"destination_bucket: {args['destination_bucket']},",
        f"stack_name: {args['stack_name']},",
        f"multiple_db_in_bucket: {args['multiple_db_in_bucket']},",
        f"allow_data_conversion: {args['allow_data_conversion']},",
        f"allow_struct_conversion: {args['allow_struct_conversion']},",
        f"webhook url: {args['webhook_url']}",
        f"channel: {args['channel']}",
        f"project: {args['project']}",
    )


if __name__ == "__main__":
    args = job_inputs()
    spark, glueContext = setup_glue(inputs=args)
    print_inputs(inputs=args)

    key = args["key"]
    key_parts = args["key"].split("/")
    project_name = key_parts[1]
    database_name = key_parts[3].replace("database_name=", "")
    table_name = key_parts[4].replace("table_name=", "")
    extraction_timestamp = key_parts[5].replace("extraction_timestamp=", "")
    filetype = os.path.splitext(args["key"])[1][1:]
    if filetype not in ["csv", "json", "jsonl"]:
        raise InvalidFileType(
            f"The filetype, {filetype} is not supported by this operation"
        )

    # Create dataframe from new file
    dynamic_frame = files_to_dynamic_frame(
        path=key,
        filetype=filetype,
        source_bucket=args["source_bucket"],
        table_name=table_name,
        allow_data_conversion=args["allow_data_conversion"],
        allow_struct_conversion=args["allow_struct_conversion"],
        extraction_timestamp=extraction_timestamp,
        glue_context=glueContext,
        spark=spark,
        args=args,
    )

    # if multiple_db_in_bucket then use
    # databasename from 'database_name=xxx' else
    # bucketname as databasename
    # CREATE  GLUE CATALOG USING BOTO
    if args["multiple_db_in_bucket"] == "True":
        db_name = project_name + "_" + database_name
    else:
        db_name = project_name

    db_name = db_name.replace("-", "_")
    print("database", db_name)

    client = boto3.client("glue")

    if not does_database_exist(client, db_name):
        print("create database")
        response = client.create_database(
            DatabaseInput={
                "Name": db_name,
                "Description": "A Glue Database for tables from " + args["stack_name"],
            }
        )

    # remove filename and raw history directory
    new_key = "/".join(args["key"].split("/")[:-2]).replace("raw_history/", "")
    desired_path = "s3://" + args["destination_bucket"] + "/" + new_key

    dynamic_frame_to_glue_catalog(
        path=desired_path,
        table_name=table_name,
        database_name=db_name,
        dynamic_frame=dynamic_frame,
        glue_context=glueContext,
    )
