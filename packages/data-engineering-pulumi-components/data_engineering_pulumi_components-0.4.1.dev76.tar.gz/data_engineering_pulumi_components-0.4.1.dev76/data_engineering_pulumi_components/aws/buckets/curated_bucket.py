from typing import Optional
from data_engineering_pulumi_components.aws.buckets.bucket import Bucket
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ResourceOptions
from pulumi_aws import Provider


class CuratedBucket(Bucket):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        lifecycle_rules_expiration_days: dict = {},
        provider: Provider = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            name=name + "-curated",
            tagger=tagger,
            lifecycle_rules=self.lifecycle_rules_expiration_days_provided(
                lifecycle_rules_expiration_days, name
            ),
            t="data-engineering-pulumi-components:aws:CuratedBucket",
            cors_rules=None,
            provider=provider,
            opts=opts,
        )
