from typing import Optional
from pulumi import ComponentResource, ResourceOptions
from data_engineering_pulumi_components.utils import Tagger
import pulumi_aws.cloudtrail as cloudtrail


class CloudTrail(ComponentResource):
    def __init__(
        self,
        name: str,
        log_landing_bucket_name: str,
        tagger: Tagger,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            name=name,
            t="data-engineering-pulumi-components:aws:LandingBucket",
            opts=opts,
        )
        self._opts = opts
        self._name = name
        self._tagger = tagger
        self._log_landing_bucket_name = log_landing_bucket_name

    def create_cloudtrail(self, field_selectors: list) -> cloudtrail.Trail:
        self.cloudtrail = cloudtrail.Trail(
            resource_name=self._name,
            opts=self._opts,
            s3_bucket_name=self._log_landing_bucket_name,
            tags=self._tagger.create_tags(name=f"{self._name}-cloudtrail"),
            advanced_event_selectors=[
                cloudtrail.TrailAdvancedEventSelectorArgs(
                    field_selectors=field_selectors,
                    name="Log Data events for buckets",
                )
            ],
        )
        return self.cloudtrail

    def build_advanced_data_event_selector(
        self,
        resources_arn_to_monitor: str,
        eventName: str,
        resources_type: str,
        eventCategory: str,
        compare_resource: str = "equals",
    ) -> list:
        """
        Function creates the list of TrailAdvancedEventSelectorFieldSelectorArgs
        dynamically

        Parameters
          ----------
          resources_arn_to_monitor : str
              The arn of the bucket(s) to monitor
          eventName: str
              Event name such as PutObject / DeleteObject
          resources_type: str
              Aws resource type such as s3, dynamodb etc
          eventCategory: str
              event category data or management event
          Returns
          -------
          list
              TrailAdvancedEventSelectorFieldSelectorArgs
        """
        _field_selectors = []
        _field_selectors.append(
            self.advanced_event_selector_field_selector(
                fieldtype="eventCategory", value=eventCategory, operator="equals"
            )
        )
        _field_selectors.append(
            self.advanced_event_selector_field_selector(
                fieldtype="eventName", value=eventName, operator="equals"
            )
        )
        _field_selectors.append(
            self.advanced_event_selector_field_selector(
                fieldtype="readOnly", value="false", operator="equals"
            )
        )
        _field_selectors.append(
            self.advanced_event_selector_field_selector(
                fieldtype="resources.type", value=resources_type, operator="equals"
            )
        )
        if resources_arn_to_monitor != "":
            _field_selectors.append(
                self.advanced_event_selector_field_selector(
                    fieldtype="resources.ARN",
                    value=resources_arn_to_monitor,
                    operator=compare_resource,
                )
            )
        return _field_selectors

    def advanced_event_selector_field_selector(
        self, fieldtype, value, operator
    ) -> cloudtrail.TrailAdvancedEventSelectorFieldSelectorArgs:
        equalto_val = [value] if operator == "equals" else None
        notequalto_val = [value] if operator == "not_equals" else None
        starts_withs_val = [value] if operator == "starts_withs" else None
        ends_withs_val = [value] if operator == "ends_withs" else None
        not_starts_withs_val = [value] if operator == "not_starts_withs" else None
        not_ends_withs_val = [value] if operator == "not_not_ends_withsequals" else None

        return cloudtrail.TrailAdvancedEventSelectorFieldSelectorArgs(
            ends_withs=ends_withs_val,
            equals=equalto_val,
            not_equals=notequalto_val,
            starts_withs=starts_withs_val,
            not_starts_withs=not_starts_withs_val,
            not_ends_withs=not_ends_withs_val,
            field=fieldtype,
        )
