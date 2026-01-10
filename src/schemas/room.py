from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class RoomCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Zа-яА-Я0-9\s\-_]+$")
    description: Optional[str] = Field(None, max_length=300)
    work_duration: int = Field(25, ge=5, le=120)
    break_duration: int = Field(5, ge=1, le=30)
    is_private: bool = False

class RoomRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    creator_id: UUID
    work_duration: int
    break_duration: int
    is_private: bool
    invite_code: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)