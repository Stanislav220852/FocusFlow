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
    
    login_password = "Fish123@"
    login_username = "Stas"
   
   
    

    login = await ac.post("/users/login",data = {
        "username": login_username,
        "password": login_password
    })
    assert login.status_code == 200
    return login.json()["access_token"]
  
    

