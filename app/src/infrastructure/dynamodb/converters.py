from typing import Any

from src.domain.mocks.schemas import MockEndpoint


def to_domain(item: dict[str, Any]) -> MockEndpoint:
    """
    DynamoDBのItemをDomain Modelに変換する。
    """
    # Pydantic V2は辞書からの変換で余分なフィールド(PK, SK等)をデフォルトで無視する設定であればそのまま渡せる。
    # しかし、明示的に必要なフィールドだけ渡すのが安全かもしれないが、
    # MockEndpointはfrozen=Trueなので、model_validateで余分なフィールドがあるとエラーになる可能性があるか？
    # ConfigDict(frozen=True) implies extra='forbid' by default? No, default is 'ignore'.
    # Let's assume 'ignore' for now.
    return MockEndpoint.model_validate(item)


def to_item(mock: MockEndpoint, pk: str, sk: str) -> dict[str, Any]:
    """
    Domain ModelをDynamoDBのItemに変換する。
    """
    # model_dump(mode='json') で Enum を str に、UUID を str に変換する
    item = mock.model_dump(mode="json")
    item["PK"] = pk
    item["SK"] = sk
    # GSI用
    item["GSI1PK"] = mock.id
    item["GSI1SK"] = "MOCK"
    return item
