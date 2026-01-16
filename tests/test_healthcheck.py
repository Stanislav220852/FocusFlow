import pytest


@pytest.mark.asyncio
async def test_health_check(ac: AsyncClient):
  
    response = await ac.get("/healthcheck") 
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"