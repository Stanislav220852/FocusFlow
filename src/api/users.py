from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserRead
from src.api.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm 
from src.services.user_services import UserService


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserRead)
async def register_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    
    return await UserService.register_new_user(db, user_data)

@user_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
   
   return  await UserService.authenticate_user(db,form_data.username,form_data.password)


@user_router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user