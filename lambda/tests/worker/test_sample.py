import json
import os
import sys
from typing import Any, Dict
from unittest.mock import Mock, patch

# テスト対象のモジュールをインポート
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from worker.Sample import hello  # noqa: E402


class TestHelloFunction:

    def setup_method(self) -> None:
        """各テストメソッドの前に実行される初期化処理"""
        self.mock_context = Mock()
        self.mock_context.aws_request_id = "test-request-id"
        self.mock_context.function_name = "test-function"
        return

    def test_hello_default_name(self) -> None:
        """nameパラメータなしでHello World が返されることを確認"""
        event: Dict[str, Any] = {}

        result = hello(event, self.mock_context)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["message"] == "Hello, World!"
        assert body["timestamp"] == "test-request-id"
        assert body["function_name"] == "test-function"

    def test_hello_with_name_parameter(self) -> None:
        """nameパラメータありで指定した名前が返されることを確認"""
        event = {"queryStringParameters": {"name": "Alice"}}

        result = hello(event, self.mock_context)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["message"] == "Hello, Alice!"
        assert body["timestamp"] == "test-request-id"
        assert body["function_name"] == "test-function"

    def test_hello_with_empty_query_parameters(self) -> None:
        """queryStringParametersが空の場合にデフォルト値が使われることを確認"""
        event: Dict[str, Any] = {}

        result = hello(event, self.mock_context)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["message"] == "Hello, World!"

    def test_hello_with_null_query_parameters(self) -> None:
        """queryStringParametersがNullの場合にデフォルト値が使われることを確認"""
        event = {"queryStringParameters": None}

        result = hello(event, self.mock_context)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["message"] == "Hello, World!"

    @patch.dict(os.environ, {"AWS_LAMBDA_FUNCTION_NAME": "prod-hello"})
    def test_hello_with_environment_variable(self) -> None:
        """環境変数が設定されている場合に正しく取得されることを確認"""
        event: Dict[str, Any] = {}

        result = hello(event, self.mock_context)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["environment"] == "prod-hello"

    def test_hello_response_headers(self) -> None:
        """レスポンスヘッダが正しく設定されることを確認"""
        event: Dict[str, Any] = {}

        result = hello(event, self.mock_context)

        expected_headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        }
        assert result["headers"] == expected_headers

    def test_hello_japanese_name(self) -> None:
        """日本語の名前でも正しく処理されることを確認"""
        event = {"queryStringParameters": {"name": "太郎"}}

        result = hello(event, self.mock_context)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["message"] == "Hello, 太郎!"
