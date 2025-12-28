from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserRead
from src.core.security import hash_password, verify_password, create_access_token
from src.api.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm 



user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserRead)
async def register_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    query2 = select(User).where(User.username == user_data.username)
    result = await db.execute(query2)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Name already registered")

    new_user = User(
        username= user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password) 
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@user_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
   
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
   
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid name or password")

    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user