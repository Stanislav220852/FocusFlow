
import pytest
import uuid



@pytest.mark.asyncio
async def test_register(ac:AsyncClient):
    unique_id = uuid.uuid4().hex[:6]
    unique_email = f"user_{unique_id}@gmail.com"
    unique_username = f"test_user_{unique_id}" 
    login_password = "Fish123@"

    response = await ac.post("/users/register",json = {
        "username": unique_username,
        "email": unique_email,
        "password": login_password
    })
    assert response.status_code == 200





@pytest.mark.asyncio
async def test_get_me(ac:AsyncClient,token:str):
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await ac.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)


@pytest.mark.asyncio
async def test_list_users(ac:AsyncClient):
    response = await ac.get("/users/list_users",params={"limit": 10, "offset": 0})
    assert response.status_code == 200
    

