import json
from pathlib import Path
from typing import Optional
from data_engineering_pulumi_components.aws.lambdas.lambda_handlers.trigger_glue import (
    trigger_glue,
)
from data_engineering_pulumi_components.utils import Tagger
from pulumi import AssetArchive, ComponentResource, FileArchive, Output, ResourceOptions
from pulumi_aws.iam import Role, RolePolicy, RolePolicyAttachment
from pulumi_aws.lambda_ import Function, FunctionEnvironmentArgs
from pulumi_aws.glue import Job


class TriggerGlueFunction(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        glue_job: Job,
        default_provider,
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        """
        Lambda function to trigger a glue job in another account and region

        Parameters
        ----------
        name : str
            The name of the resource.
        tagger : Tagger
            A tagger resource.
        opts : Optional[ResourceOptions]
            Options for the resource. By default, None.
        """
        super().__init__(
            t="data-engineering-pulumi-components:aws:TriggerGlueFunction",
            name=name,
            props=None,
            opts=opts,
        )

        self._role = Role(
            resource_name=f"{name}",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
            name=f"{name}-x-acc",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-trigger-glue"),
            opts=ResourceOptions(parent=self),
        )
        self._roleCrossAccount = Role(
            resource_name=f"{name}-x-acc",
            assume_role_policy=Output.all(self._role.arn).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"AWS": args[0]},
                                "Action": "sts:AssumeRole",
                            }
                        ],
                    }
                ),
            ),
            name=f"{name}",
            path="/service-role/",
            tags=tagger.create_tags(f"{name}-trigger-glue"),
            opts=ResourceOptions(parent=self, provider=default_provider),
        )
        self._rolePolicyCrossAccount = RolePolicy(
            resource_name=f"{name}-glue",
            name="startGetGlueJob",
            policy=Output.all(glue_job.arn).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "StartGetGlueJob",
                                "Effect": "Allow",
                                "Resource": [args[0]],
                                "Action": ["glue:StartJobRun", "glue:GetJobRun"],
                            },
                        ],
                    }
                )
            ),
            role=self._roleCrossAccount.id,
            opts=ResourceOptions(
                parent=self._roleCrossAccount, provider=default_provider
            ),
        )
        self._rolePolicyAttachmentCrossAccount = RolePolicyAttachment(
            resource_name=f"{name}-x-acc",
            policy_arn=(
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            ),
            role=self._roleCrossAccount.name,
            opts=ResourceOptions(parent=self._roleCrossAccount),
        )
        self._rolePolicy = RolePolicy(
            resource_name=f"{name}",
            name="assume-glue-role",
            policy=Output.all(self._roleCrossAccount.arn).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": {
                            "Effect": "Allow",
                            "Action": "sts:AssumeRole",
                            "Resource": [args[0]],
                        },
                    }
                )
            ),
            role=self._role.id,
            opts=ResourceOptions(parent=self._role),
        )
        self._rolePolicyAttachment = RolePolicyAttachment(
            resource_name=f"{name}-attach",
            policy_arn=(
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            ),
            role=self._role.name,
            opts=ResourceOptions(parent=self._role),
        )

        self._function = Function(
            resource_name=f"{name}-trigger",
            code=AssetArchive(
                assets={
                    ".": FileArchive(
                        path=str(Path(trigger_glue.__file__).absolute().parent)
                    )
                }
            ),
            description=Output.all(glue_job.name).apply(
                lambda args: f"Triggers glue job {args[0]}"
            ),
            environment=Output.all(
                glue_job.name, default_provider.region, self._roleCrossAccount.arn
            ).apply(
                lambda args: FunctionEnvironmentArgs(
                    variables={
                        "GLUE_JOB_NAME": args[0],
                        "JOB_REGION": args[1],
                        "CROSS_ACCOUNT_ROLE": args[2],
                    }
                )
            ),
            handler="trigger_glue.handler",
            name=f"{name}",
            role=self._role.arn,
            runtime="python3.8",
            tags=tagger.create_tags(f"{name}-trigger-glue"),
            timeout=300,
            opts=ResourceOptions(parent=self),
        )
