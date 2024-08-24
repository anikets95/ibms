import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_recommendations():
    # Simulating the addition of books
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/books", json={"title": "Book 1", "author": "Author A", "summary": "Summary A"})
        await ac.post("/books", json={"title": "Book 2", "author": "Author B", "summary": "Summary B"})

        # Now call the recommendations endpoint
        response = await ac.get("/recommendations", params={"user_preferences": "some_preferences"})

    # Test that recommendations are returned properly
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) > 0
