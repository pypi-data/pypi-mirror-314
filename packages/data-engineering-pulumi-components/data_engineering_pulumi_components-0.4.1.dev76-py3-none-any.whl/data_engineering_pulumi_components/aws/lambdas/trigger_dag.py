import json
from pathlib import Path
from typing import Optional, Union

import pulumi_aws as aws
from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.trigger_dag import (
    trigger_dag_,
)
from data_engineering_pulumi_components.utils import Tagger, BucketDetails
from pulumi import AssetArchive, ComponentResource, FileArchive, Output, ResourceOptions
from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws.lambda_ import Function, FunctionEnvironmentArgs, Permission
from pulumi_aws.s3 import BucketNotification, BucketNotificationLambdaFunctionArgs


class TriggerDagLambda(ComponentResource):
    def __init__(
        self,
        name: str,
        source_bucket: Union[Bucket, str],
        mwaa_env_name: str,
        dag_name: str,
        account_id: str,
        region: str,
        tagger: Tagger,
        prefix: str = None,
        timeout: Optional[int] = None,
        wait: Optional[int] = None,
        opts: Optional[ResourceOptions] = None,
        create_notification: bool = True,
    ) -> None:
        """
        Provides a Lambda function that triggers a DAG from a source bucket to a
        destination bucket.
        Parameters
        ----------
        name : str
            The name of the resource.
        source_bucket : Bucket
            The bucket to monitor for data uploads.
        mwaa_env_name : str
            The name of the Apache Airflow production environment (e.g. dev, prod)
        dag_name : str
            The name of the DAG to trigger in MWAA
        account_id : str
            AWS account id
        region: str
            AWS region
        tagger : Tagger
            A tagger resource.
        prefix : str, optional
            If included, only trigger DAG if file uploaded into this 'folder'.
            Don't include the trailing slash: 'project-name', not 'project-name/'
        timeout : int, optional
            Specify custom timeout value for the lambda. Defaults to 300 if not
            specified.
        wait : int, optional
            Time to wait between lambda receiving notification and then
            triggering dag. Defaults to 0 if not specified.
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        create_notification : bool
            If True, create a BucketNotification to run the Lambda when an object is
            created in the source bucket. If False, don't create a BucketNotification.
            If you have separate Lambdas for different prefixes in the same bucket,
            you'll need to set this to False and create a combined BucketNotification
            separately.
        """
        super().__init__(
            t="airflow-contracts-etl:aws:TriggerDAGFunction",
            name=name,
            props=None,
            opts=opts,
        )

        self._account_id = account_id
        self._region = region

        # If destination bucket already exists, create a BucketDetails from its name
        if isinstance(source_bucket, str):
            source_bucket_details = aws.s3.get_bucket(source_bucket)
            source_bucket_id = source_bucket_details.id
            source_bucket = BucketDetails(source_bucket)

        self._role = Role(
            resource_name=f"{name}-role",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
            name=f"{name}-trigger-dag",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-trigger-dag"),
            opts=ResourceOptions(parent=self),
        )

        # AmazonMWAAAirflowCliAccess create MWAA client token to trigger a DAG.
        # See https://docs.aws.amazon.com/mwaa/latest/userguide/samples-lambda.html
        # for more information.
        self._rolePolicy = RolePolicy(
            resource_name=f"{name}-role-policy",
            name="s3-access",
            policy=Output.all(region, account_id, mwaa_env_name).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "AmazonMWAAAirflowCliAccess",
                                "Effect": "Allow",
                                "Resource": [
                                    (
                                        f"arn:aws:airflow:{args[0]}:{args[1]}:"
                                        f"environment/{args[2]}"
                                    )
                                ],
                                "Action": ["airflow:CreateCliToken"],
                            }
                        ],
                    }
                )
            ),
            role=self._role.id,
            opts=ResourceOptions(parent=self._role),
        )

        # AWSLambdaVPCAccessExecutionRole needed to access private MWAA in the same VPC
        # See https://docs.aws.amazon.com/mwaa/latest/userguide/samples-lambda.html
        # for more information.
        self._rolePolicyAttachment = RolePolicyAttachment(
            resource_name=f"{name}-role-policy-attachment",
            policy_arn=(
                "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
            ),
            role=self._role.name,
            opts=ResourceOptions(parent=self._role),
        )

        self._function = Function(
            resource_name=f"{name}-function",
            code=AssetArchive(
                assets={
                    ".": FileArchive(
                        path=str(Path(trigger_dag_.__file__).absolute().parent)
                    )
                }
            ),
            description=Output.all(dag_name, mwaa_env_name, source_bucket.name).apply(
                lambda args: (
                    f"Triggers {args[0]} DAG in {args[1]} "
                    f"MWAA env when data is uploaded to {args[2]}"
                )
            ),
            environment=Output.all(dag_name, mwaa_env_name, wait).apply(
                lambda args: FunctionEnvironmentArgs(
                    variables={
                        "DAG_NAME": args[0],
                        "MWAA_ENV_NAME": args[1],
                        "WAIT": 0 if args[2] is None else args[2],
                    }
                )
            ),
            handler="trigger_dag_.handler",
            name=f"{name}-trigger-dag",
            role=self._role.arn,
            runtime="python3.8",
            tags=tagger.create_tags(f"{name}-trigger-dag"),
            timeout=300 if timeout is None else timeout,
            opts=ResourceOptions(parent=self),
        )

        self._permission = Permission(
            resource_name=f"{name}-permission",
            action="lambda:InvokeFunction",
            function=self._function.arn,
            principal="s3.amazonaws.com",
            source_arn=source_bucket.arn,
            opts=ResourceOptions(parent=self._function),
        )

        if create_notification:
            self._bucketNotification = BucketNotification(
                resource_name=f"{name}-bucket-notification",
                bucket=source_bucket_id,
                lambda_functions=[
                    BucketNotificationLambdaFunctionArgs(
                        events=["s3:ObjectCreated:*"],
                        lambda_function_arn=self._function.arn,
                        filter_prefix=f"{prefix}/" if prefix else None,
                    )
                ],
                opts=ResourceOptions(parent=self._permission),
            )
