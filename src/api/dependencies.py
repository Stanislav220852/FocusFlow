import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.database import get_db
from src.models.user import User
from src.core.config import settings
from src.core.security import oauth2_scheme



DBSessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(token: TokenDep, db: DBSessionDep) -> User:
   
    try:
       
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
            
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

  
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise CREDENTIALS_EXCEPTION
        
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]