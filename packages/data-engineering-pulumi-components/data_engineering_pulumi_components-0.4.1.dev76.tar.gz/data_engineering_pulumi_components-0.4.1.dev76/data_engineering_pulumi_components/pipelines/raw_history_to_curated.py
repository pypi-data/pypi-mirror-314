from typing import Optional
from data_engineering_pulumi_components.aws.glue.glue_job import GlueComponent
from data_engineering_pulumi_components.aws import (
    BucketPutPermissionsArgs,
    CopyObjectFunction,
    CuratedBucket,
    RawHistoryBucket,
)
from data_engineering_pulumi_components.aws.buckets.bucket_policy import (
    BucketPolicyBuilder,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ComponentResource, ResourceOptions
from pulumi_aws import Provider
from pulumi_aws.glue import CatalogDatabase
import os
from pathlib import Path


class RawHistoryToCuratedPipeline(ComponentResource):
    def __init__(
        self,
        name: str,
        raw_history_bucket: RawHistoryBucket,
        tagger: Tagger,
        lifecycle_rules_expiration_days: dict = {},
        add_tables_to_db: bool = False,
        default_provider: Optional[Provider] = None,
        stack_provider: Optional[Provider] = None,
        opts: Optional[ResourceOptions] = None,
        db_refresh_schedule: bool = True,
        db_refresh_on_create: bool = False,
        block_access: bool = True,
        high_memory_worker: bool = False,
        number_of_workers: int = 2,
        allow_data_conversion: str = "True",
        multiple_db_in_bucket: str = "False",
        webhook_url: str = "",
        slack_channel: str = "",
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
            lifecycle_rules_expiration_days=lifecycle_rules_expiration_days,
            provider=stack_provider,
            opts=ResourceOptions(parent=self, provider=stack_provider),
        )
        if add_tables_to_db is False:
            self._copyObjectFunction = CopyObjectFunction(
                destination_bucket=self._curatedBucket,
                name=name,
                source_bucket=raw_history_bucket,
                tagger=tagger,
                opts=ResourceOptions(parent=self),
            )

            bpb = BucketPolicyBuilder(
                Bucket=self._curatedBucket,
                put_permissions=[
                    BucketPutPermissionsArgs(
                        principal=self._copyObjectFunction._role.arn
                    )
                ],
                provider=stack_provider,
            )
            if block_access is True:
                self._curatedBucket._bucketPolicy = (
                    bpb.add_basic_access_permissions.add_access_block.build()
                )
            if block_access is False:
                self._curatedBucket._bucketPolicy = (
                    bpb.add_basic_access_permissions.build()
                )

        if add_tables_to_db is True:
            # create database if multiple_db_in_bucket option is false

            if multiple_db_in_bucket == "False":
                db_name = name.replace("-", "_")
                self._database = CatalogDatabase(
                    resource_name=f"{name}-database",
                    description=f"A Glue Database for tables from {name}",
                    name=f"{db_name}",
                    opts=ResourceOptions(provider=default_provider, retain_on_delete=True),
                )

            self._glueMoveJob = GlueComponent(
                destination_bucket=self._curatedBucket,
                name=name,
                source_bucket=raw_history_bucket,
                tagger=tagger,
                glue_script=(
                    os.path.join(
                        Path(__file__).parents[1],
                        "aws/glue/glue_move_script.py",
                    )
                ),
                glue_inputs={
                    "--source_bucket": raw_history_bucket._name,
                    "--destination_bucket": self._curatedBucket._name,
                    "--stack_name": name,
                    "--multiple_db_in_bucket": multiple_db_in_bucket,
                    "--allow_data_conversion": allow_data_conversion,
                    "--webhook_url": webhook_url,
                    "--channel": slack_channel,
                },
                default_provider=default_provider,
                stack_provider=stack_provider,
                opts=ResourceOptions(
                    parent=self,
                    depends_on=[self._curatedBucket],
                ),
                trigger_on_demand=db_refresh_on_create,
                trigger_on_schedule=db_refresh_schedule,
                high_memory_worker=high_memory_worker,
                number_of_workers=number_of_workers,
            )

            raw_history_bucket._bucketPolicy = BucketPolicyBuilder(
                Bucket=raw_history_bucket,
                put_permissions=[
                    BucketPutPermissionsArgs(principal=self._glueMoveJob._role.arn)
                ],
            ).add_glue_permissions.build()

            self._curatedBucket._bucketPolicy = BucketPolicyBuilder(
                Bucket=self._curatedBucket,
                put_permissions=[
                    BucketPutPermissionsArgs(principal=self._glueMoveJob._role.arn)
                ],
                provider=stack_provider,
            ).add_glue_permissions.build()

        if add_tables_to_db is False:
            raw_history_bucket._bucketPolicy = BucketPolicyBuilder(
                Bucket=raw_history_bucket
            ).build()
