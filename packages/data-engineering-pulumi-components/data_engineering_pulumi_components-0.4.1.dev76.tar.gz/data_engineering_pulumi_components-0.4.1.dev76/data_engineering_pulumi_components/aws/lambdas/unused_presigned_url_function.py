import json
from typing import Optional
from pathlib import Path

from pulumi import ComponentResource, ResourceOptions, AssetArchive, FileArchive
from pulumi_aws.iam import Role, RolePolicyAttachment, RolePolicy
from pulumi_aws.lambda_ import Function, Permission
from pulumi_aws.cloudwatch import EventRule, EventTarget

from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.unused_presigned_url import (
    unused_presigned_url,
)
from data_engineering_pulumi_components.utils import Tagger


class UnusedPresignedURLFunction(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            t="data-engineering-pulumi-components:aws:validateMoveObjectFunction",
            name=name,
            props=None,
            opts=opts,
        )

        self.slack_channel = "#data-engineering-alerts-prod"
        self.slack_webhook_url = "https://hooks.slack.com/services/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"

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
            name=f"{name}-unused_presigned_url",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-unused_presigned_url"),
            opts=ResourceOptions(parent=self),
        )

        self.unusedPresignedURL = Function(
            resource_name=f"{name}-function",
            name=f"{name}-unused-presigned-url",
            role=self._role.arn,
            description="Send Unused presigged URL notifications to Slack",
            runtime="python3.8",
            handler="unused_presigned_url.lambda_handler",
            code=AssetArchive(
                assets={
                    ".": FileArchive(
                        path=str(Path(unused_presigned_url.__file__).absolute().parent)
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
            tags=tagger.create_tags(f"unused-presigned-url-{name}"),
            opts=ResourceOptions(parent=self),
            timeout=300,
        )
        self._rolePolicy = RolePolicy(
            resource_name=f"{name}-role-policy",
            name="unused_presigned_url",
            policy=self.unusedPresignedURL.arn.apply(
                lambda arn: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": [
                                    "logs:Describe*",
                                    "logs:Get*",
                                    "logs:List*",
                                    "logs:StartQuery",
                                    "logs:StopQuery",
                                    "logs:TestMetricFilter",
                                    "logs:FilterLogEvents",
                                ],
                                "Effect": "Allow",
                                "Resource": "*",
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

        self._eventRule = EventRule(
            resource_name=f"{name}-unused-presigned-url",
            opts=ResourceOptions(parent=self),
            name=f"{name}-unused-presigned-url",
            description=f"Triggers the {name} lambda function to run "
            "checks if presigned urls assigned in the past hour have been used",
            schedule_expression="rate(1 hour)",
            tags=tagger.create_tags(f"{name}"),
        )
        self._eventPermission = Permission(
            resource_name=f"{name}-event-permission",
            action="lambda:InvokeFunction",
            function=self.unusedPresignedURL.arn,
            principal="events.amazonaws.com",
            source_arn=self._eventRule.arn,
            opts=ResourceOptions(parent=self.unusedPresignedURL),
        )
        self._eventTarget = EventTarget(
            resource_name=f"{name}",
            opts=ResourceOptions(parent=self._eventRule),
            arn=self.unusedPresignedURL.arn,
            rule=self._eventRule.name,
            input='{"scheduled_event": true}',
        )
