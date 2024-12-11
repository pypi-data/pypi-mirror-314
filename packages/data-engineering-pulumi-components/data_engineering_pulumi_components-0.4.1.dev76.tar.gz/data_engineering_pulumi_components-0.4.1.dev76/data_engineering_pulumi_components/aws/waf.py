import pulumi_aws as aws
from pulumi_aws import wafv2
from pulumi import ResourceOptions, ComponentResource


class WafService(ComponentResource):
    def __init__(self, service_name: str, api_stage: aws.apigateway.Stage) -> None:
        """WAF with the main free AWS common rule sets"""
        self._service_name = service_name
        self._api_stage = api_stage

        self.web_acl = wafv2.WebAcl(
            f"{self._service_name}-main-free-rule-sets",
            scope="REGIONAL",
            default_action={"Allow": {}},
            rules=[
                wafv2.WebAclRuleArgs(
                    name="AWS-AWSManagedRulesCommonRuleSet",
                    priority=1,
                    statement=wafv2.WebAclRuleStatementArgs(
                        managed_rule_group_statement=(
                            wafv2.WebAclRuleStatementManagedRuleGroupStatementArgs(
                                vendor_name="AWS",
                                name="AWSManagedRulesCommonRuleSet",
                            )
                        )
                    ),
                    override_action=wafv2.WebAclRuleOverrideActionArgs(
                        none=wafv2.WebAclRuleOverrideActionNoneArgs()
                    ),
                    visibility_config=wafv2.WebAclRuleVisibilityConfigArgs(
                        sampled_requests_enabled=True,
                        cloudwatch_metrics_enabled=True,
                        metric_name="AWS-AWSManagedRulesCommonRuleSet",
                    ),
                ),
                wafv2.WebAclRuleArgs(
                    name="AWS-AWSManagedRulesAmazonIpReputationList",
                    priority=2,
                    statement=wafv2.WebAclRuleStatementArgs(
                        managed_rule_group_statement=(
                            wafv2.WebAclRuleStatementManagedRuleGroupStatementArgs(
                                vendor_name="AWS",
                                name="AWSManagedRulesAmazonIpReputationList",
                            )
                        )
                    ),
                    override_action=wafv2.WebAclRuleOverrideActionArgs(
                        none=wafv2.WebAclRuleOverrideActionNoneArgs()
                    ),
                    visibility_config=wafv2.WebAclRuleVisibilityConfigArgs(
                        sampled_requests_enabled=True,
                        cloudwatch_metrics_enabled=True,
                        metric_name="AWS-AWSManagedRulesAmazonIpReputationList",
                    ),
                ),
                wafv2.WebAclRuleArgs(
                    name="AWS-AWSManagedRulesAnonymousIpList",
                    priority=3,
                    statement=wafv2.WebAclRuleStatementArgs(
                        managed_rule_group_statement=(
                            wafv2.WebAclRuleStatementManagedRuleGroupStatementArgs(
                                vendor_name="AWS",
                                name="AWSManagedRulesAnonymousIpList",
                            )
                        )
                    ),
                    override_action=wafv2.WebAclRuleOverrideActionArgs(
                        none=wafv2.WebAclRuleOverrideActionNoneArgs()
                    ),
                    visibility_config=wafv2.WebAclRuleVisibilityConfigArgs(
                        sampled_requests_enabled=True,
                        cloudwatch_metrics_enabled=True,
                        metric_name="AWS-AWSManagedRulesAnonymousIpList",
                    ),
                ),
                wafv2.WebAclRuleArgs(
                    name="AWS-AWSManagedRulesKnownBadInputsRuleSet",
                    priority=4,
                    statement=wafv2.WebAclRuleStatementArgs(
                        managed_rule_group_statement=(
                            wafv2.WebAclRuleStatementManagedRuleGroupStatementArgs(
                                vendor_name="AWS",
                                name="AWSManagedRulesKnownBadInputsRuleSet",
                            )
                        )
                    ),
                    override_action=wafv2.WebAclRuleOverrideActionArgs(
                        none=wafv2.WebAclRuleOverrideActionNoneArgs()
                    ),
                    visibility_config=wafv2.WebAclRuleVisibilityConfigArgs(
                        sampled_requests_enabled=True,
                        cloudwatch_metrics_enabled=True,
                        metric_name="AWS-AWSManagedRulesKnownBadInputsRuleSet",
                    ),
                ),
            ],
            visibility_config={
                "cloudwatchMetricsEnabled": True,
                "metric_name": f"{self._service_name}-uploader-waf",
                "sampledRequestsEnabled": True,
            },
        )

        self.web_acl_association = wafv2.WebAclAssociation(
            f"{self._service_name}-common-rule-set-association",
            resource_arn=self._api_stage.arn,
            web_acl_arn=self.web_acl.arn,
            opts=ResourceOptions(depends_on=[self._api_stage, self.web_acl]),
        )
