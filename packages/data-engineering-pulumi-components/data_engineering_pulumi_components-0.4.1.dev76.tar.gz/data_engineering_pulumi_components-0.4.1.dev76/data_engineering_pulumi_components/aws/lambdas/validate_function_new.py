import json
from typing import Optional
from pathlib import Path

from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.utils import Tagger
from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.notify import (
    notify_lambda_failure,
)
from pulumi import (
    AssetArchive,
    ComponentResource,
    FileArchive,
    FileAsset,
    Output,
    ResourceOptions,
)

from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws.lambda_ import (
    Function,
    FunctionEnvironmentArgs,
    Permission,
    FunctionEventInvokeConfig,
    FunctionEventInvokeConfigDestinationConfigArgs,
    FunctionEventInvokeConfigDestinationConfigOnFailureArgs,
)
from pulumi_aws.cloudwatch import EventRule, EventTarget


class ValidateMoveObjectFunction(ComponentResource):
    def __init__(
        self,
        name: str,
        bucket: Bucket,
        tagger: Tagger,
        slack_channel: str,
        slack_webhook_url: str,
        trigger_on_object_create: bool = True,
        trigger_on_schedule: bool = False,
        schedule: str = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        """
        Provides a Lambda function that inspects objects from a source bucket, and
        sends them to a pass or fail bucket depending on their response to validation
        tests.

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
        trigger_on_object_create: bool
            The lambda function is triggered when a object is created
        trigger_on_schedule: bool,
            The lambda function is triggered on a schedule
        schedule: str
            the schedule in which the lambda is triggered.
            The default is daily at midnight.
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        """
        super().__init__(
            t="data-engineering-pulumi-components:aws:validateMoveObjectFunction",
            name=name,
            props=None,
            opts=opts,
        )

        self._bucket = bucket
        self.slack_channel = slack_channel
        self.slack_webhook_url = slack_webhook_url
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
            name=f"{name}-validate",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-validate"),
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
                                "Sid": "GetDeleteSourceDirectory",
                                "Effect": "Allow",
                                "Resource": [
                                    f"{args[0]}/landing/*/data/*",
                                    f"{args[0]}/landing/*/data/",
                                ],
                                "Action": [
                                    "s3:GetObject*",
                                    "s3:DeleteObject*",
                                ],
                            },
                            {
                                "Sid": "AllowListLandingDirectory",
                                "Action": ["s3:ListBucket"],
                                "Effect": "Allow",
                                "Resource": [args[0]],
                                "Condition": {
                                    "StringEquals": {"s3:prefix": ["", "landing/"]}
                                },
                            },
                            {
                                "Sid": "PutPassDirectory",
                                "Effect": "Allow",
                                "Resource": [f"{args[0]}/raw_history/*/data/*"],
                                "Action": ["s3:PutObject*"],
                            },
                            {
                                "Sid": "PutFailDirectory",
                                "Effect": "Allow",
                                "Resource": [f"{args[0]}/fail/*/data/*"],
                                "Action": ["s3:PutObject*"],
                            },
                            {
                                "Sid": "InvokeDestinationFunction",
                                "Effect": "Allow",
                                "Resource": "*",
                                "Action": "lambda:InvokeFunction",
                            },
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
                        str(Path(__file__).parent.absolute())
                        + "/lambda_handlers/validate/dependencies.zip"
                    ),
                    "validate.py": FileAsset(
                        str(Path(__file__).parent.absolute())
                        + "/lambda_handlers/validate/validate_new.py"
                    ),
                }
            ),
            description=Output.all(bucket.name).apply(
                lambda args: f"Validates data from {args[0]}"
            ),
            environment=Output.all(
                bucket.name,
                self.slack_channel,
                self.slack_webhook_url,
            ).apply(
                lambda name: FunctionEnvironmentArgs(
                    variables={
                        "SOURCE_BUCKET": f"{name[0]}",
                        "CHANNEL": f"{name[1]}",
                        "WEBHOOK_URL": f"{name[2]}",
                    }
                )
            ),
            handler="validate.handler",
            name=f"{name}-validate",
            role=self._role.arn,
            runtime="python3.8",
            tags=tagger.create_tags(f"{name}-validate"),
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
        self._permission = Permission(
            resource_name=f"{name}-permission",
            action="lambda:InvokeFunction",
            function=self._function.arn,
            principal="s3.amazonaws.com",
            source_arn=bucket.arn,
            opts=ResourceOptions(parent=self._function),
        )

        if trigger_on_object_create:
            self._eventRule = EventRule(
                resource_name=f"{self._name}-validate",
                opts=ResourceOptions(parent=self),
                name=f"{self._name}-validate",
                description=f"Triggers the {name} lambda function to re-run "
                f"validation and move files from landing to raw_history for {self._name}",
                event_pattern=Output.all(bucket.id).apply(
                    lambda args: json.dumps(
                        {
                            "source": ["aws.s3"],
                            "detail-type": ["Object Created"],
                            "detail": {
                                "bucket": {"name": [args[0]]},
                                "object": {
                                    "key": [
                                        {"prefix": "landing/"}
                                    ]
                                },
                            },
                        }
                    )
                ),
                tags=tagger.create_tags(f"{self._name}"),
            )

            self._eventPermission = Permission(
                resource_name=f"{name}-validate",
                action="lambda:InvokeFunction",
                function=self._function.arn,
                principal="events.amazonaws.com",
                source_arn=self._eventRule.arn,
                opts=ResourceOptions(parent=self._function),
            )
            self._eventTarget = EventTarget(
                resource_name=f"{name}-validate",
                opts=ResourceOptions(parent=self._eventRule),
                arn=self._function.arn,
                rule=self._eventRule.name,
                input_path="$.detail",
            )

        if trigger_on_schedule:
            if schedule is None:
                schedule = "cron(0 0 ? * * *)"  # Every day at 00:00 UTC

            self._eventRule = EventRule(
                resource_name=f"{name}-run-validation-and-move",
                opts=ResourceOptions(parent=self),
                name=f"{name}-run-validation-and-move",
                description=f"Triggers the {name} lambda function to re-run "
                "validation and move files from landing to raw history",
                schedule_expression=schedule,
                tags=tagger.create_tags(f"{name}"),
            )

            self._eventPermission = Permission(
                resource_name=f"{name}-validate",
                action="lambda:InvokeFunction",
                function=self._function.arn,
                principal="events.amazonaws.com",
                source_arn=self._eventRule.arn,
                opts=ResourceOptions(parent=self._function),
            )
            self._eventTarget = EventTarget(
                resource_name=f"{name}-validate",
                opts=ResourceOptions(parent=self._eventRule),
                arn=self._function.arn,
                rule=self._eventRule.name,
                input='{"scheduled_event": true}',
            )
        self._functionEventInvokeConfig = FunctionEventInvokeConfig(
            resource_name=f"{name}-function-event-config",
            function_name=self._function,
            destination_config=FunctionEventInvokeConfigDestinationConfigArgs(
                on_failure=FunctionEventInvokeConfigDestinationConfigOnFailureArgs(
                    destination=self._notifyLambdaFailure.arn
                )
            ),
        )
