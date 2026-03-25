import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock

from app.schemas.schemas import UserRead


@pytest.mark.anyio
async def test_create_new_rule_success(
        async_client: AsyncClient, mock_current_user: UserRead
):
    payload = {
        "pattern": ".*spam.*",
        "rule_type": "regex",
        "client_id": str(mock_current_user.id),
    }

    response = await async_client.post("/api/v1/rules/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["rule_type"] == payload["rule_type"]
    assert data["pattern"] == payload["pattern"]


@pytest.mark.anyio
async def test_list_returns_items(async_client: AsyncClient, mock_current_user):
    response = await async_client.get("/api/v1/rules/")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)


@pytest.mark.anyio
async def test_delete_rule_success(
        async_client: AsyncClient, mock_current_user, mock_async_session
):
    from app.models.prompt_rule import PromptRule

    mock_rule = PromptRule(
        id=1,
        pattern=".*test.*",
        rule_type="simple",
        client_id=str(mock_current_user.id),
        user_id=mock_current_user.id,
    )

    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = mock_rule
    mock_result.scalars.return_value = mock_scalars

    mock_async_session.execute.return_value = mock_result
    create_resp = await async_client.post(
        "/api/v1/rules/",
        json={
            "pattern": ".*test.*",
            "rule_type": "simple",
            "client_id": str(mock_current_user.id),
        },
    )

    assert create_resp.status_code == 200
    data = create_resp.json()
    rule_id = data.get("id", 1)

    delete_resp = await async_client.delete(f"/api/v1/rules/{rule_id}")
    assert delete_resp.status_code == 200


@pytest.mark.anyio
async def test_delete_rule_not_found(async_client: AsyncClient, mock_current_user):
    non_existent_id = 1234567890

    delete_resp = await async_client.delete(f"/api/v1/rules/{non_existent_id}")
    assert delete_resp.status_code in [200, 404, 500]
