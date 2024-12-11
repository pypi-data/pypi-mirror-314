from typing import Optional
from data_engineering_pulumi_components.aws import CuratedBucket, Bucket
from data_engineering_pulumi_components.aws.buckets.bucket_policy_new import (
    BucketPolicyBuilder,
    BucketPutPermissionsArgs,
)
from data_engineering_pulumi_components.aws.lambdas.monitoring import (
    MonitorPipelineFunction,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import Output, ComponentResource, ResourceOptions
from pulumi_aws import Provider


class DeployMonitoringPipeline(ComponentResource):
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
        slack_webhook_url: str = "",
        slack_channel: str = "",
    ) -> None:
        super().__init__(
            t=(
                "data-engineering-pulumi-components:monitor:" "DeployMonitoringPipeline"
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
        self.monitoring_lambdas = {}

        # Create a specific function for each project
        self.monitoring_lambdas = [
            MonitorPipelineFunction(
                bucket=self._curatedBucket,
                name=f"{name}-{project}",
                slack_channel=slack_channel,
                slack_webhook_url=slack_webhook_url,
                tagger=tagger,
                prefix=project,
                opts=ResourceOptions(parent=self),
            )
            for project, config in project_configs_dict.items()
            if config["freshness_monitoring"] is True
        ]
        self.monitoring_lambda_role_arns = Output.all(
            [
                monitoring_lambda._role.arn
                for monitoring_lambda in self.monitoring_lambdas
            ]
        )[0]

        bpb = BucketPolicyBuilder(
            Bucket=self._curatedBucket,
            put_permissions=[
                BucketPutPermissionsArgs(principal=self.monitoring_lambda_role_arns)
            ],
        )

        if block_access is True:
            self._curatedBucket._bucketPolicy = (
                bpb.add_basic_access_permissions.add_glue_permissions.add_lambda_read_permissions.add_access_block.build()
            )
        else:
            self._curatedBucket._bucketPolicy = (
                bpb.add_basic_access_permissions.add_glue_permissions.add_lambda_read_permissions.build()
            )
