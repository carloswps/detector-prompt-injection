from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_analyze_returns_success(async_client: AsyncClient, mocker):
    payload = {"prompt": "Qual a capital da França?"}

    mock_analyze = mocker.patch(
        "app.services.detector_service.DetectorService.analyze_and_log",
        new_callable=AsyncMock,
    )
    mock_analyze.return_value = {"status": "success", "risk_score": 0.05}

    response = await async_client.post("/api/v1/chat/analyze", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "success", "risk_score": 0.05}

    mock_analyze.assert_awaited_once()
