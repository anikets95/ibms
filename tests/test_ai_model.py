from unittest.mock import AsyncMock

import pytest
from app.routers import ai_model

@pytest.mark.asyncio
async def test_generate_summary():
    mock_model = AsyncMock()
    mock_model.generate_summary.return_value = "Generated summary"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/generate-summary", json={"content": "This is a test book content."})

    assert response.status_code == 200
    assert response.json()["summary"] == "Generated summary"
