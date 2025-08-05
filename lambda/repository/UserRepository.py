import logging
import os
from typing import Any, Dict, List

from library.dynamo import DynamoDBClient


class UserRepository:
    def __init__(self) -> None:
        self.client = DynamoDBClient()
        self.dynamodb = self.client.connect()
        self.table_name = os.environ.get("USERS_TABLE")
        self.table = self.dynamodb.Table(self.table_name)
        self.logger = logging.getLogger(__name__)

    def get_all_users(self) -> List[Dict[str, Any]]:
        """全ユーザー取得"""
        try:
            response = self.table.scan()
            items = response.get("Items", [])

            users = []
            for item in items:
                users.append(
                    {
                        "id": int(item["id"]),
                        "name": item["name"],
                        "email": item["email"],
                    }
                )

            return users
        except Exception as e:
            self.logger.error(f"Error finding all users: {str(e)}")
            raise
