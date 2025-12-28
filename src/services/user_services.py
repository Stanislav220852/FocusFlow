from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm 
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import hash_password, verify_password, create_access_token



class UserService:
    @staticmethod
    async def register_new_user(db: AsyncSession, user_data: UserCreate):
        query_email = select(User).where(User.email == user_data.email)
        result = await db.execute(query_email)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
    
        query_name = select(User).where(User.username == user_data.username)
        result = await db.execute(query_name)
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
        

    @staticmethod
    async def authenticate_user(db: AsyncSession, username,password):
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
   
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid name or password")

    
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
        
