import re
from typing import Optional, Sequence
import pulumi_aws.s3 as s3
from pulumi_aws.s3 import BucketCorsRuleArgs
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ComponentResource, ResourceOptions
from pulumi_aws import Provider
import pulumi_aws as aws


class InvalidBucketNameError(Exception):
    pass


def _bucket_name_is_valid(name: str) -> bool:
    """
    Checks if an S3 bucket name is valid.

    See https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html

    Parameters
    ----------
    name : str
        The name of the bucket.

    Returns
    -------
    bool
        If the name is valid.
    """
    match = re.match(
        pattern=(
            # ensure name is between 3 and 63 characters long
            r"(?=^.{3,63}$)"
            # ensure name is not formatted like an IP address
            r"(?!^(\d+\.)+\d+$)"
            # match zero or more labels followed by a single period
            r"(^(([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)*"
            # ensure final label doesn't end in a period or dash
            r"([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$)"
        ),
        string=name,
    )
    if match:
        return True
    else:
        return False


class Bucket(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        cors_rules: BucketCorsRuleArgs = None,
        t: Optional[str] = None,
        lifecycle_rules: Sequence[s3.BucketLifecycleRuleArgs] = None,
        versioning: Optional[s3.BucketVersioningArgs] = None,
        provider: Provider = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        if t is None:
            t = "data-engineering-pulumi-components:aws:Bucket"
        super().__init__(
            t=t,
            name=name,
            props=None,
            opts=opts,
        )
        if not isinstance(name, str):
            raise TypeError("name must be of type str")
        if not isinstance(tagger, Tagger):
            raise TypeError("tagger must be of type Tagger")

        if not _bucket_name_is_valid(name=name):
            raise InvalidBucketNameError("name is not valid")

        self._name = name

        self._bucket = s3.Bucket(
            resource_name=f"{name}-bucket",
            acl=s3.CannedAcl.PRIVATE,
            cors_rules=cors_rules,
            bucket=name,
            force_destroy=True,
            lifecycle_rules=lifecycle_rules,
            server_side_encryption_configuration={
                "rule": {
                    "apply_server_side_encryption_by_default": {
                        "sse_algorithm": "AES256"
                    }
                }
            },
            tags=tagger.create_tags(name=name),
            versioning=versioning,
            opts=ResourceOptions(parent=self)
            if provider is None
            else ResourceOptions(parent=self, provider=provider),
        )

        self._bucketPublicAccessBlock = s3.BucketPublicAccessBlock(
            resource_name=f"{name}-bucket-public-access-block",
            bucket=self._bucket.id,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True,
            opts=ResourceOptions(parent=self._bucket),
        )

        outputs = {
            "arn": self._bucket.arn,
            "id": self._bucket.id,
            "name": self._bucket.bucket,
        }

        for name, value in outputs.items():
            setattr(self, name, value)

        self.register_outputs(outputs)

    def lifecycle_rules_expiration_days_provided(
        self, lifecycle_rules_expiration_days, name
    ):
        if bool(lifecycle_rules_expiration_days) is False:
            return None
        if bool(lifecycle_rules_expiration_days) is True:
            policies = []
            for prefix, days in lifecycle_rules_expiration_days.items():
                policy = aws.s3.BucketLifecycleRuleArgs(
                    id="bucket-lifecycle-" + name + "-" + prefix,
                    enabled=True,
                    prefix=prefix,
                    expiration=aws.s3.BucketLifecycleRuleExpirationArgs(
                        days=days, expired_object_delete_marker=True
                    ),
                    noncurrent_version_expiration=(
                        aws.s3.BucketLifecycleRuleNoncurrentVersionExpirationArgs(
                            days=days,
                        )
                    ),
                )
                policies.append(policy)

            return policies

    def add_cors_rules(
        self,
        cors_allowed_headers: list,
        cors_allowed_origins: list,
    ):
        return [
            BucketCorsRuleArgs(
                allowed_headers=cors_allowed_headers,
                allowed_methods=[
                    "PUT",
                    "POST",
                ],
                allowed_origins=cors_allowed_origins,
                expose_headers=[
                    "x-amz-server-side-encryption",
                    "x-amz-request-id",
                    "x-amz-id-2",
                ],
                max_age_seconds=3000,
            )
        ]
