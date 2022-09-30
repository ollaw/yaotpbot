import json

from pulumi_aws import dynamodb, iam

tags = {"app": "yaotpbot", "env": "production"}

table = dynamodb.Table(
    "yaotpbot-table",
    name="yaotpbot-table",
    attributes=[
        dynamodb.TableAttributeArgs(
            name="id",
            type="S",
        ),
        dynamodb.TableAttributeArgs(
            name="name",
            type="S",
        ),
    ],
    billing_mode="PROVISIONED",
    hash_key="id",
    range_key="name",
    read_capacity=5,
    write_capacity=5,
    tags=tags,
)


user = iam.User("yaotpbot", name="yaotpbot", tags=tags)
ak = iam.AccessKey("yaotpbot-ak", user=user.name)
policy = iam.UserPolicy(
    "yaotpbot-dynamo-policy",
    name="yaotpbot-dynamo-policy",
    user=user.name,
    policy=table.arn.apply(
        lambda arn: json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "Stmt1661462886736",
                        "Action": [
                            "dynamodb:DeleteItem",
                            "dynamodb:DescribeTable",
                            "dynamodb:GetItem",
                            "dynamodb:GetRecords",
                            "dynamodb:PutItem",
                            "dynamodb:Query",
                            "dynamodb:Scan",
                            "dynamodb:UpdateItem",
                            "dynamodb:UpdateTimeToLive",
                        ],
                        "Effect": "Allow",
                        "Resource": arn,
                    }
                ],
            }
        ),
    ),
)
