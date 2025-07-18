import json
import logging
import os
from typing import Any, Dict

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def create_response_with_headers(
    status_code: int, body: Dict[str, Any], headers: Dict[str, str]
) -> Dict[str, Any]:
    """カスタムヘッダー付きのAPI Gateway用レスポンスを生成"""
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    }

    default_headers.update(headers)

    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body, ensure_ascii=False),
    }


def hello(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Hello World エンドポイント"""

    try:
        logger.info(f"Event: {json.dumps(event)}")

        # クエリパラメータから名前を取得
        query_params = event.get("queryStringParameters") or {}
        name = query_params.get("name", "World")

        response_body = {
            "message": f"Hello, {name}!",
            "timestamp": context.aws_request_id,
            "function_name": context.function_name,
            "environment": os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "local"),
        }

        logger.info(f"Response: {response_body}")
        return create_response(200, response_body)

    except Exception as e:
        logger.error(f"Error in hello function: {str(e)}")
        return create_response(500, {"error": "Internal server error"})


def get_users(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """ユーザー一覧取得エンドポイント"""
    try:
        logger.info(f"Event: {json.dumps(event)}")

        # サンプルユーザーデータ
        users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
        ]

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
    try:
        logger.info(f"Event: {json.dumps(event)}")

        # パスパラメータからIDを取得
        path_params = event.get("pathParameters") or {}
        user_id = path_params.get("id")

        if not user_id:
            return create_response(400, {"error": "User ID is required"})

        try:
            user_id = int(user_id)
        except ValueError:
            return create_response(400, {"error": "Invalid user ID format"})

        # サンプルユーザーデータ（実際にはDBから取得）
        users = {
            1: {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "role": "admin",
            },
            2: {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
            3: {
                "id": 3,
                "name": "Charlie",
                "email": "charlie@example.com",
                "role": "user",
            },
        }

        user = users.get(user_id)
        if not user:
            return create_response(404, {"error": "User not found"})

        response_body = {"user": user, "timestamp": context.aws_request_id}

        logger.info(f"Returning user: {user}")
        return create_response(200, response_body)

    except Exception as e:
        logger.error(f"Error in get_user function: {str(e)}")
        return create_response(500, {"error": "Internal server error"})
