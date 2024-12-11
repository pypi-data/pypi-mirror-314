import json
import pulumi_aws as aws
from pulumi import ComponentResource, Output, ResourceOptions
from typing import Sequence, Optional, Union
from data_engineering_pulumi_components.utils import (
    validate_principal,
    is_anonymous_user,
)


class AnonymousUserError(Exception):
    pass


class BucketPutPermissionsArgs:
    def __init__(
        self,
        principal: Union[str, Output],
        paths: Optional[Sequence[str]] = None,
        allow_anonymous_users: Optional[bool] = True,
    ) -> None:
        # We can't validate principals passed as Output types – these will always only
        # come from Pulumi resources so they should always be valid and shouldn't be
        # anonymous users
        if not isinstance(principal, Output):
            validate_principal(principal)
            if is_anonymous_user(principal) and not allow_anonymous_users:
                raise AnonymousUserError("anonymous users are not allowed")
        self.principal = principal
        if paths:
            if not isinstance(paths, list):
                raise TypeError("paths must be of type list")
            for path in paths:
                if not isinstance(path, str):
                    raise TypeError("Each path must be of type str")
                if not path.startswith("/") or not path.endswith("/"):
                    raise ValueError("Each path must start and end with '/'")
        self.paths = paths


class BucketPolicyBuilder(ComponentResource):
    def __init__(
        self,
        Bucket,
        put_permissions: Optional[Sequence[BucketPutPermissionsArgs]] = None,
        provider: aws.Provider = None,
    ):
        """
        Pass a bucket and some permissions to this object to build a bucket policy and
        attach it to a bucket.
        """
        if getattr(Bucket, "_put_permissions", None) is not None:
            raise Exception("put_permissions are already set")

        self.Bucket_facade = Bucket
        self._put_permissions = put_permissions
        self._statements = []
        self._provider = provider

    @property
    def add_basic_access_permissions(
        self,
    ):
        self._statements = Output.all(
            bucket_arn=self.Bucket_facade._bucket.arn,
            **{str(i): item.__dict__ for i, item in enumerate(self._put_permissions)}
            if self._put_permissions
            else {},
        ).apply(self._get_basic_access_policy)

        return self

    def _get_basic_access_policy(self, args):
        bucket_arn = args.pop("bucket_arn")

        all_principals = []
        statements = []
        for item in args.values():
            principal = item["principal"]
            paths = item["paths"]
            all_principals.append(principal)
            statements.extend(
                [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": [principal]},
                        "Action": ["s3:PutObject", "s3:PutObjectAcl"],
                        "Resource": [bucket_arn + path + "*" for path in paths]
                        if paths
                        else [bucket_arn + "/*"],
                    }
                ]
            )
        statements.extend(
            [
                {
                    "Effect": "Deny",
                    "Principal": {"AWS": all_principals},
                    "Action": ["s3:PutObject"],
                    "Resource": [bucket_arn + "/*"],
                    "Condition": {
                        "StringNotEquals": {
                            "s3:x-amz-acl": ["bucket-owner-full-control"],
                        },
                    },
                },
                {
                    "Effect": "Deny",
                    "Principal": {"AWS": all_principals},
                    "Action": ["s3:PutObject"],
                    "Resource": [bucket_arn + "/*"],
                    "Condition": {
                        "StringNotEquals": {
                            "s3:x-amz-server-side-encryption": ["AES256"],
                        },
                    },
                },
                {
                    "Effect": "Deny",
                    "Principal": {"AWS": all_principals},
                    "Action": ["s3:PutObject"],
                    "Resource": [bucket_arn + "/*"],
                    "Condition": {
                        "Null": {"s3:x-amz-server-side-encryption": ["true"]},
                    },
                },
            ]
        )

        return statements

    @property
    def add_glue_permissions(self):
        self._glue_statements = Output.all(
            bucket_arn=self.Bucket_facade._bucket.arn,
            **{str(i): item.__dict__ for i, item in enumerate(self._put_permissions)}
            if self._put_permissions
            else {},
        ).apply(self._get_policy_glue)

        self._statements = Output.all(
            statements=self._statements,
            glue_statements=self._glue_statements,
        ).apply(lambda args: args.pop("statements") + args.pop("glue_statements"))

        return self

    def _get_policy_glue(self, args):
        bucket_arn = args.pop("bucket_arn")

        all_principals = []
        statements = []
        for item in args.values():
            principal = item["principal"]
            paths = item["paths"]
            all_principals.append(principal)
            statements.append(
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": [principal]},
                    "Action": [
                        "s3:Get*",
                        "s3:Put*",
                        "s3:Delete*",
                        "s3:ListBucket",
                        "s3:ListBucketMultipartUploads",
                        "s3:ListBucketVersions",
                        "s3:ListMultipartUploadParts",
                    ],
                    "Resource": [bucket_arn + path for path in paths]
                    + [bucket_arn + path + "*" for path in paths]
                    if paths
                    else [bucket_arn, bucket_arn + "/*"],
                }
            )

        return statements

    @property
    def add_access_block(self):
        self._access_block_statements = Output.all(
            bucket_arn=self.Bucket_facade._bucket.arn,
            **{str(i): item.__dict__ for i, item in enumerate(self._put_permissions)}
            if self._put_permissions
            else {},
        ).apply(self._access_block_policy)

        self._statements = Output.all(
            statements=self._statements,
            access_block_statements=self._access_block_statements,
        ).apply(
            lambda args: args.pop("statements") + args.pop("access_block_statements")
        )

        return self

    def _access_block_policy(self, args):
        bucket_arn = args.pop("bucket_arn")
        statements = []
        for item in args.values():
            paths = item["paths"]
            statements.extend(
                [
                    {
                        "Effect": "Deny",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:*",
                        "Resource": [bucket_arn + path for path in paths]
                        + [bucket_arn + path + "*" for path in paths]
                        if paths
                        else [bucket_arn, bucket_arn + "/*"],
                        "Condition": {"StringLike": {"aws:PrincipalArn": "*/alpha_*"}},
                    },
                ]
            )

        return statements

    @property
    def add_cloud_trail_permissions(self):
        self._cloudtrail_statements = Output.all(
            bucket_arn=self.Bucket_facade._bucket.arn,
        ).apply(self._get_cloudtrail_policy)

        self._statements = Output.all(
            statements=self._statements,
            cloudtrail_statements=self._cloudtrail_statements,
        ).apply(lambda args: args.pop("statements") + args.pop("cloudtrail_statements"))

        return self

    def _get_cloudtrail_policy(self, args):
        bucket_arn = args.pop("bucket_arn")

        return [
            {
                "Sid": "AWSCloudTrailAclCheck",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": bucket_arn,
            },
            {
                "Sid": "AWSCloudTrailWrite",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": bucket_arn + "/*",
                "Condition": {
                    "StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}
                },
            },
        ]

    def _add_ssl_requests_only(self):
        self._ssl_requests_only_statements = Output.all(
            bucket_arn=self.Bucket_facade._bucket.arn,
        ).apply(self._get_ssl_requests_only_policy)

        self._statements = Output.all(
            statements=self._statements,
            ssl_requests_only_statements=self._ssl_requests_only_statements,
        ).apply(
            lambda args: args.pop("statements")
            + args.pop("ssl_requests_only_statements")
        )

        return self

    def _get_ssl_requests_only_policy(self, args):
        bucket_arn = args.pop("bucket_arn")

        return [
            {
                "Sid": "AllowSSLRequestsOnly",
                "Action": "s3:*",
                "Effect": "Deny",
                "Resource": [bucket_arn, bucket_arn + "/*"],
                "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                "Principal": "*",
            }
        ]

    def _get_final_policy_doc(self):
        # All bucket should deny non SSL requests
        self._add_ssl_requests_only()
        # Every operation to an Output object needs to be an apply or a Pulumi function
        return self._statements.apply(
            lambda l: json.dumps({"Version": "2012-10-17", "Statement": l})
        )

    def _create_bucket_policy(self, policy_doc: Output):
        # Some of the glue outputs aren't compatible with direct reference in the
        # bucket policy creation, so it all needs to be wrapped in an output object.

        # Aas of 2022-08-13 Pulumi can't handle replacing bucket policies
        # Behaviour has been observed that even with delete_before_replace, Pulumi will
        # create the new bucket policy first, then delete the old one, resulting in a
        # blank policy on the attached bucket.
        # Deleting then creating in separate commands works.
        return Output.all(
            name=self.Bucket_facade._name,
            bucket_id=self.Bucket_facade._bucket.id,
            policy_doc=policy_doc,
            bucket=self.Bucket_facade._bucket,
            provider=self._provider,
        ).apply(
            lambda args: aws.s3.BucketPolicy(
                resource_name=f"{args['name']}-bucket-policy",
                bucket=args["bucket_id"],
                policy=args["policy_doc"],  # needs to be json)
                opts=ResourceOptions(
                    parent=args["bucket"],
                    depends_on=args["bucket"],
                    delete_before_replace=True,
                )
                if args["provider"] is None
                else ResourceOptions(
                    parent=args["bucket"],
                    depends_on=args["bucket"],
                    provider=args["provider"],
                    delete_before_replace=True,
                ),
            )
        )

    def build(self):
        self._policy_doc = self._get_final_policy_doc()
        self._policy = self._create_bucket_policy(self._policy_doc)
        # Tag the bucket with put permissions so another policy is not added
        self.Bucket_facade._put_permissions = self._put_permissions

        return self._policy
