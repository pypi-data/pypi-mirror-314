import json
from typing import Optional
from data_engineering_pulumi_components.utils import Tagger
from pulumi import ComponentResource, ResourceOptions
from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws import Provider


class CreateGetFieldsRole(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        region: str,
        account_id: str,
        data_stack_provider: Provider,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        """
        Role to allow listing fields in a glue table.

        name : str
            The name of the resource.
        tagger : Tagger
            A tagger resource.
        region : str
        account_id: str
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        """

        super().__init__(
            t="data-engineering-pulumi-components:aws:CreateGetFieldsRole",
            name=name,
            props=None,
            opts=opts,
        )

        self._region = region
        self._account_id = account_id

        self.lambdarole = Role(
            resource_name=f"{name}-lambda-role",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        },
                    ],
                }
            ),
            name=f"{name}-lambda-role",
            path="/service-role/",
            tags=tagger.create_tags(name=f"{name}-lambda-role"),
            opts=ResourceOptions(parent=self, provider=data_stack_provider),
        )

        self._rolePolicy = RolePolicy(
            resource_name=f"{name}-policy",
            name=f"{name}-lambda-policy",
            policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "GetTables",
                            "Effect": "Allow",
                            "Action": [
                                "glue:GetDatabase",
                                "glue:GetTables",
                                "glue:GetDatabases",
                                "glue:GetTable",
                            ],
                            "Resource": "*",
                        }
                    ],
                }
            ),
            role=self.lambdarole.id,
            opts=ResourceOptions(parent=self.lambdarole, provider=data_stack_provider),
        )

        self._rolePolicyAttachment = RolePolicyAttachment(
            resource_name=f"{name}-role-policy-attachment",
            policy_arn=(
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            ),
            role=self.lambdarole.name,
            opts=ResourceOptions(provider=data_stack_provider),
        )
