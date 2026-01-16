from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserRead
from src.api.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm 
from src.services.user_services import UserService
from src.api.dependencies import DBSessionDep,CurrentUserDep
from typing import List
from uuid import UUID

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserRead)
async def register_user(
    user_data: UserCreate, 
    db: DBSessionDep
):
    
    return await UserService.register_new_user(db, user_data)

@user_router.post("/login")
async def login(
    db: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
    
):
   
   return  await UserService.authenticate_user(db,form_data.username,form_data.password)


@user_router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.get("/list_user",response_model=List[UserRead])
async def list_user(
    db: DBSessionDep,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await UserService.list_users(db, limit, offset)

@user_router.get("/{user_id}",response_model=UserRead)
async def get_user(
    db:DBSessionDep,
    user_id:UUID
):
    return await UserService.get_user_by_id(db,user_id)


