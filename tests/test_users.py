
import pytest
import uuid

@pytest.mark.asyncio
async def test_get_me(ac:AsyncClient,token:str):
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await ac.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)