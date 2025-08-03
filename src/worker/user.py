import json
import logging
import os
import sys
from typing import Any, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from library.dynamo import DynamoDBClient  # noqa: E402


def get_users(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """ユーザー一覧取得エンドポイント"""

    # ログ設定
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # DynamoDBクライアント初期化
    client = DynamoDBClient()
    dynamodb = client.connect()
    TABLE_NAME = os.environ.get("USERS_TABLE")
    if TABLE_NAME is None:
        raise ValueError("USERS_TABLE environment variable is not set")
    table = dynamodb.Table(TABLE_NAME)

    try:
        logger.info(f"Event: {json.dumps(event)}")

        # DynamoDBからユーザー一覧を取得
        response = table.scan()
        items = response.get("Items", [])

        # DynamoDBのデータ形式を変換
        users = []
        for item in items:
            users.append(
                {"id": int(item["id"]), "name": item["name"], "email": item["email"]}
            )

        response_body = {
            "users": users,
            "count": len(users),
            "timestamp": context.aws_request_id,
        }

        logger.info(f"Returning {len(users)} users")
        return create_response(200, response_body)

    except Exception as e:
        logger.error(f"Error in get_users function: {str(e)}")
        return create_response(500, {"error": "Internal server error"})


def get_user(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """特定ユーザー取得エンドポイント"""

    # ログ設定
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # DynamoDBクライアント初期化
    client = DynamoDBClient()
    dynamodb = client.connect()
    TABLE_NAME = os.environ.get("USERS_TABLE")
    if TABLE_NAME is None:
        raise ValueError("USERS_TABLE environment variable is not set")
    table = dynamodb.Table(TABLE_NAME)

    try:
        logger.info(f"Event: {json.dumps(event)}")

        path_params = event.get("pathParameters") or {}
        user_id = path_params.get("id")

        if not user_id:
            return create_response(400, {"error": "User ID is required"})

        try:
            user_id = int(user_id)
        except ValueError:
            return create_response(400, {"error": "Invalid user ID format"})

        # DynamoDBから特定ユーザーを取得
        response = table.get_item(Key={"id": str(user_id)})
        item = response.get("Item")

        if not item:
            return create_response(404, {"error": "User not found"})

        user = {
            "id": int(item["id"]),
            "name": item["name"],
            "email": item["email"],
        }

        response_body = {"user": user, "timestamp": context.aws_request_id}

        logger.info(f"Returning user: {user}")
        return create_response(200, response_body)

    except Exception as e:
        logger.error(f"Error in get_user function: {str(e)}")
        return create_response(500, {"error": "Internal server error"})


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """API Gateway用のレスポンスを生成"""
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    }

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body, ensure_ascii=False),
    }
