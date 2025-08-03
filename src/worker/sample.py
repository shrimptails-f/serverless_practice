import json
import logging
import os
import sys
from typing import Any, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def hello(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Hello World エンドポイント"""

    # ログ設定
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Event: {json.dumps(event)}")

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
