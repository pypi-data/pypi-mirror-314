from typing import Optional

from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.aws.buckets.bucket_policy import (
    BucketPolicyBuilder,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ResourceOptions


class CloudTrailLogBucket(Bucket):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            name=name,
            t="data-engineering-pulumi-components:aws:CloudTrailLogBucket",
            tagger=tagger,
            opts=opts,
        )
        self.policy = BucketPolicyBuilder(
            Bucket=self
        ).add_cloud_trail_permissions.build()
