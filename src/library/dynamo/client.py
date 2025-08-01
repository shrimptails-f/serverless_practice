import os

import boto3
from boto3.resources.base import ServiceResource


class DynamoDBClient:
    is_local = False

    def __init__(self) -> None:
        """
        DynamoDBクライアントを初期化
        """

        stage = os.environ.get("STAGE", "dev")
        if stage == "dev":
            self.is_local = True

    def connect(self) -> ServiceResource:
        """
        DynamoDBリソースを生成

        Returns:
            ServiceResource: DynamoDBリソース
        """
        if self.is_local:
            # ローカル環境設定
            dynamodb = boto3.resource(
                "dynamodb",
                endpoint_url=os.environ.get(
                    "DYNAMODB_ENDPOINT_URL", "http://localstack:4566"
                ),
                region_name=os.environ.get("AWS_REGION", "ap-northeast-1"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
            )
        else:
            # 本番環境設定
            params = {"region_name": os.environ.get("AWS_REGION", "ap-northeast-1")}
            endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
            if endpoint_url:
                params["endpoint_url"] = endpoint_url
                params["aws_access_key_id"] = os.environ.get(
                    "AWS_ACCESS_KEY_ID", "test"
                )
                params["aws_secret_access_key"] = os.environ.get(
                    "AWS_SECRET_ACCESS_KEY", "test"
                )

            dynamodb = boto3.resource("dynamodb", **params)

        return dynamodb
