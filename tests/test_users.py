
import pytest
import uuid

@pytest.mark.asyncio
async def test_register(ac:AsyncSession):
    unique_email = f"user_{uuid.uuid4().hex[:6]}@gmail.com"
    payload = {
        "username": f"test_user_{uuid.uuid4().hex[:6]}",
        "email": unique_email,
        "password": "Password123!"
    }

    response = await ac.post("/users/register",json = payload)

    assert response.status_code == 200
    

