from pathlib import Path
from typing import Optional

from data_engineering_pulumi_components.utils import Tagger
from pulumi import AssetArchive, ComponentResource, FileArchive, ResourceOptions
import pulumi_aws as aws
from pulumi_aws.lambda_ import Function, FunctionEnvironmentArgs, Permission
from data_engineering_pulumi_components.aws import get_fields


class GetFieldsLambda(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        glue_prefix: str,
        account_id: str,
        region: str,
        api: aws.apigateway,
        resource_path: str,
        lambda_role_arn: str,
        data_stack_provider,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        """
        Provide a Lambda function that gets a list of all the fields in a table.
        Parameters
        ----------
        name : str
            The name of the resource.
        tagger : Tagger
            A tagger resource.
        glue_prefix : str
            Prefix to find the right db on glue
        account_id : str,
            The account number for creation of resources.
        region : str,
            Region the resources to be created.
        api : aws.apigateway,
            The API which uses the lambda to read the list of fields.
        resource_path : str,
            API resource path.
        lambda_role_arn : str
            Lambda role arn for the function to use.
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        """
        super().__init__(
            t="data-engineering-pulumi-components:aws:GetFieldsFunction",
            name=name,
            props=None,
            opts=opts,
        )

        self._glue_prefix = glue_prefix
        self._region = region
        self._account_id = account_id
        self._resource_path = resource_path
        self._lambda_role_arn = lambda_role_arn

        self.function = Function(
            resource_name=f"{name}-function",
            code=AssetArchive(
                assets={
                    ".": FileArchive(
                        path=str(Path(get_fields.__file__).absolute().parent)
                    )
                }
            ),
            description="Return list of fields in a table.",
            role=self._lambda_role_arn,
            handler="get_fields.handler",
            environment=FunctionEnvironmentArgs(
                variables={"glue_prefix": self._glue_prefix}
            ),
            runtime="python3.8",
            tags=tagger.create_tags(f"{name}-get-fields"),
            timeout=300,
            opts=ResourceOptions(parent=self, provider=data_stack_provider),
        )

        self._permission = Permission(
            resource_name=f"{name}-get-fields-permission",
            principal="apigateway.amazonaws.com",
            action="lambda:InvokeFunction",
            function=self.function.arn,
            source_arn=api.id.apply(
                lambda api_id: f"arn:aws:execute-api:{self._region}:"
                + f"{self._account_id}:{api_id}/*/GET/{self._resource_path}"
            ),
            opts=ResourceOptions(parent=self.function, provider=data_stack_provider),
        )
