from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from main import app
from app.api.deps import get_current_user
from app.core.database import get_db


@pytest.fixture
def mock_async_session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def override_get_db(mock_async_session):
    async def _dependency():
        yield mock_async_session

    return _dependency


@pytest.fixture
def mock_current_user() -> MagicMock:
    return MagicMock(id=1, email="teste@gmail.com")


@pytest.fixture
def mock_detector_service():
    return MagicMock()


@pytest.fixture
def mock_rule_service():
    return MagicMock()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def async_client(
        override_get_db,
        mock_current_user,
):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    from httpx import ASGITransport

    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
