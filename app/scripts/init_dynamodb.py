import os

import boto3
from botocore.exceptions import ClientError


def init_dynamodb() -> None:
    """
    Initialize DynamoDB table for local development.
    """
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    print(f"Connecting to DynamoDB at {endpoint_url}...")

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )

    table_name = "MockTable"

    try:
        table = dynamodb.Table(table_name)
        table.load()
        print(f"Table '{table_name}' already exists.")
        return
    except ClientError:
        pass

    print(f"Creating table '{table_name}'...")

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "GSI1PK", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GSI-ID",
                    "KeySchema": [{"AttributeName": "GSI1PK", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        print(f"Table '{table_name}' created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    init_dynamodb()
