from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def check_password_complexity(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[0-9]", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return value

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    xp: int
    level: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
