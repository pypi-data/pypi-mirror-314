from typing import Optional
from data_engineering_pulumi_components.aws.glue.glue_job_new import GluePipeline
from data_engineering_pulumi_components.aws import CuratedBucket, Bucket
from data_engineering_pulumi_components.aws.lambdas.copy_object_function_new import (
    CopyObjectFunction,
)
from data_engineering_pulumi_components.aws.buckets.bucket_policy_new import (
    BucketPolicyBuilder,
    BucketPutPermissionsArgs,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import Output, ComponentResource, ResourceOptions
from pulumi_aws import Provider
import os
from pathlib import Path


class RawHistoryToCuratedPipeline(ComponentResource):
    def __init__(
        self,
        name: str,
        data_eng_bucket: Bucket,
        project_configs_dict: dict,
        tagger: Tagger,
        default_provider: Optional[Provider] = None,
        stack_provider: Optional[Provider] = None,
        opts: Optional[ResourceOptions] = None,
        block_access: bool = True,
        webhook_url: str = "",
        slack_channel: str = ""
    ) -> None:
        super().__init__(
            t=(
                "data-engineering-pulumi-components:pipelines:"
                "RawHistoryToCuratedPipeline"
            ),
            name=name,
            props=None,
            opts=opts,
        )
        self._curatedBucket = CuratedBucket(
            name=name,
            tagger=tagger,
            provider=stack_provider,
            opts=ResourceOptions(parent=self, provider=stack_provider),
        )
        self.copy_lambdas = {}
        self.glue_jobs = {}

        # Create a specific copy function or glue job for each project
        self.copy_lambdas = [
            CopyObjectFunction(
                destination_bucket=self._curatedBucket,
                name=f"{name}-{project}",
                source_bucket=data_eng_bucket,
                tagger=tagger,
                prefix=project,
                opts=ResourceOptions(parent=self),
            )
            for project, config in project_configs_dict.items()
            if config["create_glue_registration"] is False
        ]
        self.copy_lambda_role_arns = Output.all(
            [copy_lambda._role.arn for copy_lambda in self.copy_lambdas]
        )[0]

        self.glue_components = [
            GluePipeline(
                destination_bucket=self._curatedBucket,
                name=f"{name}-{project}",
                project=project,
                source_bucket=data_eng_bucket,
                tagger=tagger,
                glue_script=(
                    os.path.join(
                        Path(__file__).parents[1],
                        "aws/glue/glue_move_script_new.py",
                    )
                ),
                glue_inputs={
                    "--source_bucket": data_eng_bucket._name,
                    "--destination_bucket": self._curatedBucket._name,
                    "--stack_name": name,
                    "--multiple_db_in_bucket": config.get(
                        "multiple_db_in_bucket", "False"
                    ),
                    "--allow_data_conversion": "False",
                    "--allow_struct_conversion": str(config.get(
                        "allow_struct_conversion", "False"
                    )),
                    "--webhook_url": webhook_url,
                    "--channel": slack_channel,
                    "--project": project,
                },
                default_provider=default_provider,
                stack_provider=stack_provider,
                opts=ResourceOptions(
                    parent=self,
                    depends_on=[self._curatedBucket],
                ),
                high_memory_worker=config.get("high_memory_workers", False),
                number_of_workers=config.get("number_of_workers", 2),
            )
            for project, config in project_configs_dict.items()
            if config["create_glue_registration"] is True
        ]

        self.glue_role_arns = Output.all(
            [glue_component._role.arn for glue_component in self.glue_components]
        )[0]

        self._data_eng_bucket_policy = BucketPolicyBuilder(
            Bucket=data_eng_bucket,
            put_permissions=[
                BucketPutPermissionsArgs(
                    principal=config["arn"],
                    paths=[
                        f"/landing/{project}/data/",
                        f"/landing/{project}/logs/",
                        f"/landing/{project}/metadata/",
                    ],
                    allow_anonymous_users=False,
                )
                for project, config in project_configs_dict.items()
            ]
            if project_configs_dict
            else None,
            glue_put_permissions=[
                BucketPutPermissionsArgs(principal=self.glue_role_arns),
            ],
        ).add_basic_access_permissions.add_glue_permissions.build()

        bpb = BucketPolicyBuilder(
            Bucket=self._curatedBucket,
            put_permissions=[
                BucketPutPermissionsArgs(principal=self.copy_lambda_role_arns)
            ],
            glue_put_permissions=[
                BucketPutPermissionsArgs(principal=self.glue_role_arns)
            ],
            provider=stack_provider,
        )

        if block_access is True:
            self._curatedBucket._bucketPolicy = (
                bpb.add_basic_access_permissions.add_glue_permissions.add_access_block.build()
            )
        if block_access is False:
            self._curatedBucket._bucketPolicy = (
                bpb.add_basic_access_permissions.add_glue_permissions.build()
            )
