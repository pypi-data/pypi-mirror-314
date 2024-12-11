import json
from pathlib import Path
from typing import Optional, Union

from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.copy import copy_
from data_engineering_pulumi_components.utils import Tagger, BucketDetails
from pulumi import AssetArchive, ComponentResource, FileArchive, Output, ResourceOptions
from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws.lambda_ import Function, FunctionEnvironmentArgs, Permission
from pulumi_aws.cloudwatch import EventRule, EventTarget


class CopyObjectFunction(ComponentResource):
    def __init__(
        self,
        destination_bucket: Union[Bucket, str],
        name: str,
        source_bucket: Bucket,
        tagger: Tagger,
        prefix: str = None,
        opts: Optional[ResourceOptions] = None,
        create_notification: bool = True,
    ) -> None:
        """
        Provides a Lambda function that copies objects from a source bucket to a
        destination bucket.

        Parameters
        ----------
        destination_bucket : Bucket, str
            The bucket to copy data to, if created in this stack. Or if the bucket
            already exists, its name as a string.
        name : str
            The name of the resource.
        source_bucket : Bucket
            The bucket to copy data from.
        tagger : Tagger
            A tagger resource.
        prefix : str, optional
            If included, only copy files from this 'folder'.
            Don't include the trailing slash: 'project-name', not 'project-name/'
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
            t="data-engineering-pulumi-components:aws:CopyObjectFunction",
            name=name,
            props=None,
            opts=opts,
        )

        # If destination bucket already exists, create a BucketDetails from its name
        if isinstance(destination_bucket, str):
            destination_bucket = BucketDetails(destination_bucket)

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
            name=f"{name}-copy",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-copy"),
            opts=ResourceOptions(parent=self),
        )
        self._rolePolicy = RolePolicy(
            resource_name=f"{name}-role-policy",
            name="s3-access",
            policy=Output.all(source_bucket.arn, destination_bucket.arn, prefix).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "GetSourceBucket",
                                "Effect": "Allow",
                                "Resource": [f"{args[0]}/raw_history/{args[2]}/data/*"],
                                "Action": ["s3:GetObject*"],
                            },
                            {
                                "Sid": "PutDestinationBucket",
                                "Effect": "Allow",
                                "Resource": [f"{args[1]}/{args[2]}/data/*"],
                                "Action": ["s3:PutObject*"],
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
            resource_name=f"{name}-copy-function",
            code=AssetArchive(
                assets={
                    ".": FileArchive(path=str(Path(copy_.__file__).absolute().parent))
                }
            ),
            description=Output.all(source_bucket.name, destination_bucket.name).apply(
                lambda args: f"Copies data from {args[0]} to {args[1]}"
            ),
            environment=Output.all(destination_bucket.name).apply(
                lambda args: FunctionEnvironmentArgs(
                    variables={"DESTINATION_BUCKET": args[0]}
                )
            ),
            handler="copy_.handler",
            name=f"{name}-copy",
            role=self._role.arn,
            runtime="python3.8",
            tags=tagger.create_tags(f"{name}-copy"),
            timeout=300,
            opts=ResourceOptions(parent=self),
        )
        self._permission = Permission(
            resource_name=f"{name}-copy-permission",
            action="lambda:InvokeFunction",
            function=self._function.arn,
            principal="s3.amazonaws.com",
            source_arn=source_bucket.arn,
            opts=ResourceOptions(parent=self._function),
        )
        if create_notification:
            self._eventRule = EventRule(
                resource_name=f"{prefix}-copy",
                opts=ResourceOptions(parent=self),
                name=f"{prefix}-copy",
                description=f"Triggers the {name} lambda function to re-run "
                f"validation and move files from raw history to curated for {prefix}",
                event_pattern=Output.all(source_bucket.id, prefix).apply(
                    lambda args: json.dumps(
                        {
                            "source": ["aws.s3"],
                            "detail-type": ["Object Created"],
                            "detail": {
                                "bucket": {"name": [args[0]]},
                                "object": {
                                    "key": [{"prefix": f"raw_history/{prefix}/data"}]
                                },
                            },
                        }
                    )
                ),
                tags=tagger.create_tags(f"{prefix}"),
            )

            self._eventPermission = Permission(
                resource_name=f"{name}-copy-event-permission",
                action="lambda:InvokeFunction",
                function=self._function.arn,
                principal="events.amazonaws.com",
                source_arn=self._eventRule.arn,
                opts=ResourceOptions(parent=self._function),
            )
            self._eventTarget = EventTarget(
                resource_name=f"{name}-copy",
                opts=ResourceOptions(parent=self._eventRule),
                arn=self._function.arn,
                rule=self._eventRule.name,
                input_path="$.detail",
            )
