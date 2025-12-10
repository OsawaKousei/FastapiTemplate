import asyncio
from typing import Any

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.domain.mocks.repository import MockRepository
from src.domain.mocks.schemas import HttpMethod, MockEndpoint
from src.infrastructure.dynamodb.client import get_table
from src.infrastructure.dynamodb.converters import to_domain, to_item


class DynamoMockRepository:
    """
    DynamoDB implementation of MockRepository.
    Uses Single Table Design with PK=MOCK#{method}#{path} and SK=METADATA.
    Uses GSI-ID (PK=GSI1PK) for ID-based lookups.
    """

    def __init__(self, table_name: str = "MockTable") -> None:
        self._table = get_table(table_name)

    async def save(self, mock: MockEndpoint) -> None:
        pk = self._build_pk(mock.method, mock.path)
        sk = self._build_sk()
        item = to_item(mock, pk, sk)

        await asyncio.to_thread(self._table.put_item, Item=item)

    async def find(self, method: HttpMethod, path: str) -> MockEndpoint | None:
        pk = self._build_pk(method, path)
        sk = self._build_sk()

        response = await asyncio.to_thread(
            self._table.get_item, Key={"PK": pk, "SK": sk}
        )
        item = response.get("Item")
        if item:
            return to_domain(item)
        return None

    async def delete(self, mock_id: str) -> bool:
        # First find the item by ID to get PK/SK needed for deletion
        mock = await self.find_by_id(mock_id)
        if not mock:
            return False

        pk = self._build_pk(mock.method, mock.path)
        sk = self._build_sk()

        try:
            await asyncio.to_thread(self._table.delete_item, Key={"PK": pk, "SK": sk})
            return True
        except ClientError:
            return False

    async def find_by_id(self, mock_id: str) -> MockEndpoint | None:
        # Use GSI for ID lookup
        response = await asyncio.to_thread(
            self._table.query,
            IndexName="GSI-ID",
            KeyConditionExpression=Key("GSI1PK").eq(mock_id),
        )
        items = response.get("Items", [])
        if items:
            return to_domain(items[0])
        return None

    async def find_all(self) -> list[MockEndpoint]:
        # Scan the table to get all mocks
        # In a real production scenario with many items, this should be paginated
        response = await asyncio.to_thread(self._table.scan)
        items = response.get("Items", [])
        return [to_domain(item) for item in items]

    def _build_pk(self, method: str, path: str) -> str:
        return f"MOCK#{method}#{path}"

    def _build_sk(self) -> str:
        return "METADATA"
