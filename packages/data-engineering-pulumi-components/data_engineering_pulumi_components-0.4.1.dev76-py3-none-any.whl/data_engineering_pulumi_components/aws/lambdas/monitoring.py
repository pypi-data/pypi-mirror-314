import json
from typing import Optional
from pathlib import Path

from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.utils import Tagger
from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.notify import (
    notify_lambda_failure,
)
from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.monitoring import (
    monitor_curated,
)
from pulumi import (
    AssetArchive,
    ComponentResource,
    FileArchive,
    Output,
    ResourceOptions,
)

from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws.lambda_ import (
    Function,
    FunctionEnvironmentArgs,
    Permission,
)
from pulumi_aws.cloudwatch import EventRule


class MonitorPipelineFunction(ComponentResource):
    def __init__(
        self,
        name: str,
        bucket: Bucket,
        tagger: Tagger,
        slack_channel: str,
        slack_webhook_url: str,
        pipeline_name: str,
        schedule: str = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        """
        Provides a Lambda function that monitors the freshness of files
        landing in a bucket

        Parameters
        ----------
        name : str
            The name of the resource.
        bucket : Bucket
            The bucket to copy data from.
        tagger : Tagger
            A tagger resource.
        slack_channel: str
            The name of the Slack channel receiving alerts
        slack_webhook_url: str
            Slack's webhook URL
        schedule: str
            the schedule in which the lambda is triggered.
            Default is daily at 5am.
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        """
        super().__init__(
            t="data-engineering-pulumi-components:aws:MonitorPipelinesFunction",
            name=name,
            props=None,
            opts=opts,
        )

        self._bucket = bucket
        self.slack_channel = slack_channel
        self.slack_webhook_url = slack_webhook_url
        self.pipeline_name = pipeline_name

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
            name=f"{name}-monitor",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-monitor"),
            opts=ResourceOptions(parent=self),
        )
        self._rolePolicy = RolePolicy(
            resource_name=f"{name}-role-policy",
            name="s3-access",
            policy=Output.all(bucket.arn).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "ListAndGetObjects",
                                "Effect": "Allow",
                                "Action": ["s3:ListBucket", "s3:GetObject"],
                                "Resource": [args[0], f"{args[0]}/*"],
                            }
                        ],
                    }
                )
            ),
            role=self._role.id,
            opts=ResourceOptions(parent=self._role),
        )
        self._rolePolicyAttachment = RolePolicyAttachment(
            resource_name=f"{name}-role-policy-attachment",
            policy_arn=(
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            ),
            role=self._role.name,
            opts=ResourceOptions(parent=self._role),
        )
        self._function = Function(
            resource_name=f"{name}-function",
            code=AssetArchive(
                assets={
                    ".": FileArchive(
                        path=str(Path(monitor_curated.__file__).absolute().parent)
                    )
                }
            ),
            description=Output.all(bucket.name).apply(
                lambda args: f"Monitors freshness of data for each pipeline in {args[0]}"
            ),
            environment=Output.all(
                bucket.name,
                self.slack_channel,
                self.slack_webhook_url,
                self.pipeline_name,
            ).apply(
                lambda name: FunctionEnvironmentArgs(
                    variables={
                        "SOURCE_BUCKET": f"{name[0]}",
                        "CHANNEL": f"{name[1]}",
                        "WEBHOOK_URL": f"{name[2]}",
                        "PIPELINE_NAME": f"{name[3]}",
                    }
                )
            ),
            handler="monitor_curated.handler",
            name=f"{name}-monitor",
            role=self._role.arn,
            runtime="python3.8",
            tags=tagger.create_tags(f"{name}-monitor"),
            timeout=300,
            opts=ResourceOptions(parent=self),
        )
        self._notifyLambdaFailure = Function(
            resource_name=f"notify-lambda-failure-{name}",
            name=f"notify-lambda-failure-{name}",
            role=self._role.arn,
            description="Send Lambda Failure notifications to Slack",
            runtime="python3.8",
            handler="notify_lambda_failure.handler",
            code=AssetArchive(
                assets={
                    ".": FileArchive(
                        path=str(Path(notify_lambda_failure.__file__).absolute().parent)
                    )
                }
            ),
            environment=(
                {
                    "variables": {
                        "CHANNEL": self.slack_channel,
                        "WEBHOOK_URL": self.slack_webhook_url,
                    }
                }
            ),
            tags=tagger.create_tags(f"notify-lambda-failure-{name}"),
            opts=ResourceOptions(parent=self),
            timeout=300,
        )

        if schedule is None:
            schedule = "cron(*/10 * * * * *)"  # Every 10 minutes for testing

        self._eventRule = EventRule(
            resource_name=f"{name}-run-monitoring-check",
            opts=ResourceOptions(parent=self),
            name=f"{name}-run-monitoring-check",
            description=f"Triggers the {name} lambda function to re-run "
            "monitoring function",
            schedule_expression=schedule,
            tags=tagger.create_tags(f"{name}"),
        )

        self._eventPermission = Permission(
            resource_name=f"{name}-monitoring",
            action="lambda:InvokeFunction",
            function=self._function.arn,
            principal="events.amazonaws.com",
            source_arn=self._eventRule.arn,
            opts=ResourceOptions(parent=self._function),
        )
