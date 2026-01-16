import pytest
from httpx import AsyncClient, ASGITransport
from main import app 
import uuid

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope= "function")
async def token(ac:AsyncClient) -> str:
    unique_id = uuid.uuid4().hex[:6]
    unique_email = f"user_{unique_id}@gmail.com"
    unique_username = f"test_user_{unique_id}" 
    login_password = "Fish123@"
    login_username = "Stas"
   
   

    await ac.post("/users/register",json = {
        "username": unique_username,
        "email": unique_email,
        "password": login_password
    })
    

    login = await ac.post("/users/login",data = {
        "username": login_username,
        "password": login_password
    })
    assert login.status_code == 200
    return login.json()["access_token"]
  
    

