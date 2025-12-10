import os
from typing import Any

import boto3


def get_dynamodb_resource() -> Any:
    """
    DynamoDBリソースを取得する。
    環境変数 DYNAMODB_ENDPOINT_URL が設定されている場合は、そのエンドポイントを使用する。
    """
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL")
    if endpoint_url:
        return boto3.resource("dynamodb", endpoint_url=endpoint_url)
    return boto3.resource("dynamodb")


def get_table(table_name: str) -> Any:
    """
    DynamoDBテーブルリソースを取得する。
    """
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)
