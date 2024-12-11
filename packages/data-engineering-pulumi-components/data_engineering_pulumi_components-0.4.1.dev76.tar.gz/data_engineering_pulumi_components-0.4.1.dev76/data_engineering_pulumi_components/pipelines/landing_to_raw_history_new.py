from typing import Optional

from data_engineering_pulumi_components.aws import (
    Bucket,
)
from data_engineering_pulumi_components.aws.lambdas.validate_function_new import (
    ValidateMoveObjectFunction,
)
from pulumi_aws.s3 import BucketCorsRuleArgs, BucketNotification
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ComponentResource, ResourceOptions


class LandingToRawHistoryPipeline(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        slack_channel: str,
        slack_webhook_url: str,
        move_on_object_create: bool = True,
        move_on_schedule: bool = False,
        schedule: str = None,
        cors_allowed_headers: list = None,
        cors_allowed_origins: list = None,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            t=(
                "data-engineering-pulumi-components:pipelines:"
                "LandingToRawHistoryPipeline"
            ),
            name=name,
            props=None,
            opts=opts,
        )

        self._data_eng_bucket = Bucket(
            name=name,
            tagger=tagger,
            cors_rules=(
                [
                    BucketCorsRuleArgs(
                        allowed_headers=cors_allowed_headers,
                        allowed_methods=["PUT", "POST"],
                        allowed_origins=cors_allowed_origins,
                        expose_headers=[
                            "x-amz-server-side-encryption",
                            "x-amz-request-id",
                            "x-amz-id-2",
                        ],
                        max_age_seconds=3000,
                    )
                ]
                if cors_allowed_headers and cors_allowed_origins
                else None
            ),
            opts=ResourceOptions(parent=self),
        )

        self._bucketNotification = BucketNotification(
            f"{self._data_eng_bucket._name}-Notification",
            bucket=self._data_eng_bucket._bucket.id,
            eventbridge=True,
        )

        self._validate_move_object_function = ValidateMoveObjectFunction(
            name=name,
            bucket=self._data_eng_bucket,
            opts=ResourceOptions(
                parent=self,
                depends_on=[self._data_eng_bucket],
            ),
            trigger_on_object_create=move_on_object_create,
            trigger_on_schedule=move_on_schedule,
            schedule=schedule,
            tagger=tagger,
            slack_channel=slack_channel,
            slack_webhook_url=slack_webhook_url,
        )
