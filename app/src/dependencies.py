from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.domain.mocks.repository import MockRepository
from src.domain.mocks.services import MockManagementService, MockSimulatorService
from src.domain.mocks.template_engine import TemplateEngine
from src.infrastructure.dynamodb.mock_repository import DynamoMockRepository


@lru_cache
def get_repository() -> MockRepository:
    """
    Provides a singleton instance of the MockRepository.
    Uses DynamoMockRepository implementation.
    """
    return DynamoMockRepository()


@lru_cache
def get_template_engine() -> TemplateEngine:
    """
    Provides a singleton instance of the TemplateEngine.
    """
    return TemplateEngine()


def get_mock_mgmt_service(
    repo: Annotated[MockRepository, Depends(get_repository)],
) -> MockManagementService:
    """
    Provides an instance of MockManagementService with repository injected.
    """
    return MockManagementService(repo)


def get_mock_sim_service(
    repo: Annotated[MockRepository, Depends(get_repository)],
    template_engine: Annotated[TemplateEngine, Depends(get_template_engine)],
) -> MockSimulatorService:
    """
    Provides an instance of MockSimulatorService with repository and template engine
    injected.
    """
    return MockSimulatorService(repo, template_engine)
