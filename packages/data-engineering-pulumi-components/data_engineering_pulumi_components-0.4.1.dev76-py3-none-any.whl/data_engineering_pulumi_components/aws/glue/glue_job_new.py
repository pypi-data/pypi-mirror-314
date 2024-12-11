import json
from typing import Optional

from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.utils import Tagger
from pulumi import (
    ComponentResource,
    Output,
    ResourceOptions,
    FileAsset,
)
from data_engineering_pulumi_components.aws.lambdas.trigger_glue_function import (
    TriggerGlueFunction,
)
from pulumi_aws import Provider
from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws.glue import (
    Job,
    JobArgs,
    JobCommandArgs,
    JobExecutionPropertyArgs,
    SecurityConfiguration,
)
from pulumi_aws.cloudwatch import EventRule, EventTarget
from pulumi_aws.s3 import BucketObject
from pulumi_aws.lambda_ import Permission


class GluePipeline(ComponentResource):
    def __init__(
        self,
        destination_bucket: Bucket,
        name: str,
        source_bucket: Bucket,
        tagger: Tagger,
        glue_script: str,
        glue_inputs: dict,
        project: str = None,
        default_provider: Optional[Provider] = None,
        stack_provider: Optional[Provider] = None,
        high_memory_worker: bool = False,
        number_of_workers: int = 2,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        """
        Provides a Glue Component that copies objects from a source bucket to a
        destination bucket as a parquet file.

        Parameters
        ----------
        destination_bucket : Bucket
            The bucket to copy data to.
        name : str
            The name of the resource.
        source_bucket : Bucket
            The bucket to copy data from.
        tagger : Tagger
            A tagger resource.
        glue_script: str
            File path leading to a valid glue script for the job to run.
        glue_inputs: dict
            A dict that contains the inputs for the provided glue script
        default_provider: Optional[Provider]
            A Provider for the Glue Components
        stack_provider: Optional[Provider]
            A Provider for the roles related to Curated Bucket
            Provider specified in stack config, usually the bucket component
        test_trigger : bool
            In the test environment, the trigger has to go off immediately for tests
            to pass. This, when set to true, will cause an immediate trigger rather
            than a scheduled one. Defaults to False (and thus a 3am schedule).
        high_memory_node: bool
            Worker type. This is by default is G.1X but if some stack needs
            high memory node it can be switched to G.2X
        number_of_workers: int
            By Default the number of workers are set to 2. It can increased
            based on the data size it needs to be processed.
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        """
        super().__init__(
            t="data-engineering-pulumi-components:aws:GlueMoveJob",
            name=name,
            props=None,
            opts=opts,
        )
        self._name = name
        self._role = Role(
            resource_name=f"{name}-role",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "glue.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
            name=f"{name}-glue",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-glue-role"),
            opts=ResourceOptions(parent=self, provider=stack_provider),
        )
        self._rolePolicy = RolePolicy(
            resource_name=f"{name}-role-policy",
            name="AWSGlueServiceRole-Glue-s3-access",
            policy=Output.all(source_bucket.arn, destination_bucket.arn, project).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "GetPutDeleteSourceBucket",
                                "Effect": "Allow",
                                "Resource": [
                                    f"{args[0]}/raw_history/{args[2]}",
                                    f"{args[0]}/raw_history/{args[2]}/*",
                                ]
                                if args[2]
                                else [
                                    f"{args[0]}/raw_history",
                                    f"{args[0]}/raw_history/*",
                                ],
                                "Action": [
                                    "s3:GetObject*",
                                    "s3:PutObject*",
                                    "s3:DeleteObject*",
                                ],
                            },
                            {
                                "Sid": "ListSourceBucket",
                                "Effect": "Allow",
                                "Resource": args[0],
                                "Action": [
                                    "s3:ListBucket",
                                ],
                            },
                            {
                                "Sid": "GetPutDeleteDestinationBucket",
                                "Effect": "Allow",
                                "Resource": [
                                    f"{args[1]}/{args[2]}",
                                    f"{args[1]}/{args[2]}/*",
                                ]
                                if args[2]
                                else [f"{args[1]}/", f"{args[1]}/*"],
                                "Action": [
                                    "s3:GetObject*",
                                    "s3:PutObject*",
                                    "s3:DeleteObject*",
                                ],
                            },
                            {
                                "Sid": "ListDestinationBucket",
                                "Effect": "Allow",
                                "Resource": args[1],
                                "Action": [
                                    "s3:ListBucket",
                                ],
                            },
                        ],
                    }
                ),
            ),
            role=self._role.id,
            opts=ResourceOptions(parent=self._role, provider=default_provider),
        )
        self._rolePolicyAttachment = RolePolicyAttachment(
            resource_name=f"{name}",
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole",
            role=self._role.name,
            opts=ResourceOptions(parent=self._role, provider=default_provider),
        )
        self._glueJobScript = BucketObject(
            resource_name=f"{name}",
            opts=ResourceOptions(
                depends_on=[self._rolePolicy], provider=stack_provider
            ),
            acl="bucket-owner-full-control",
            bucket=destination_bucket.name,
            key=f"glue-job-scripts/{project}-{glue_script.split('/')[-1]}"
            if project
            else f"glue-job-scripts/{glue_script.split('/')[-1]}",
            server_side_encryption="AES256",
            source=FileAsset(glue_script),
            tags=tagger.create_tags(f"{name}-glue-script"),
        )
        self._securityConfiguration = SecurityConfiguration(
            resource_name=f"{name}-sc",
            opts=ResourceOptions(parent=self, provider=default_provider),
            encryption_configuration={
                "cloudwatch_encryption": {"cloudwatch_encryption_mode": "DISABLED"},
                "job_bookmarks_encryption": {
                    "job_bookmarks_encryption_mode": "DISABLED"
                },
                "s3_encryption": {"s3_encryption_mode": "SSE-S3"},
            },
            name=f"{name}-sc",
        )

        # The job dictates the glue catalog region, for all of AP this should be ireland
        self._job = Job(
            resource_name=f"{name}",
            args=JobArgs(
                command=JobCommandArgs(
                    script_location=Output.all(
                        self._glueJobScript.bucket, self._glueJobScript.key
                    ).apply(lambda o: f"s3://{o[0]}/{o[1]}"),
                ),
                role_arn=self._role.arn,
                default_arguments=glue_inputs,
                description=f"Populates the {name} curated bucket with parquets",
                execution_property=JobExecutionPropertyArgs(max_concurrent_runs=100),
                max_retries=4,
                timeout=360,
                glue_version="4.0",
                name=f"{name}",
                number_of_workers=number_of_workers,
                security_configuration=self._securityConfiguration.name,
                tags=tagger.create_tags(f"{name}-glue-job"),
                worker_type="G.2X" if high_memory_worker else "G.1X",
            ),
            opts=ResourceOptions(
                parent=self,
                depends_on=[
                    self._glueJobScript,
                    self._role,
                    self._securityConfiguration,
                ],
                provider=default_provider,
            ),
        )

        self._lambda_trigger = TriggerGlueFunction(
            name=name,
            tagger=tagger,
            glue_job=self._job,
            default_provider=default_provider,
        )

        self._eventRule = EventRule(
            resource_name=f"{name}-load",
            opts=ResourceOptions(parent=self),
            name=f"{name}-load",
            description=f"Triggers the {name} lambda function to trigger glue",
            event_pattern=Output.all(source_bucket.id, project).apply(
                lambda args: json.dumps(
                    {
                        "source": ["aws.s3"],
                        "detail-type": ["Object Created"],
                        "detail": {
                            "bucket": {"name": [args[0]]},
                            "object": {
                                "key": [{"prefix": f"raw_history/{project}/data"}]
                            },
                        },
                    }
                )
            ),
            tags=tagger.create_tags(f"{project}"),
        )

        self._eventPermission = Permission(
            resource_name=f"{name}-perm",
            action="lambda:InvokeFunction",
            function=self._lambda_trigger._function.arn,
            principal="events.amazonaws.com",
            source_arn=self._eventRule.arn,
            opts=ResourceOptions(parent=self._lambda_trigger._function),
        )
        self._eventTarget = EventTarget(
            resource_name=f"{name}",
            opts=ResourceOptions(parent=self._eventRule),
            arn=self._lambda_trigger._function.arn,
            rule=self._eventRule.name,
            input_path="$.detail",
        )
