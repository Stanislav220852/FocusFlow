from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class FocusSessionCreate(BaseModel):
    room_id: UUID
    duration_minutes: int = Field(25, ge=5, le=240, description="Длительность от 5 до 240 минут")

class FocusSessionRead(BaseModel):
    id: UUID
    room_id: UUID
    started_at: datetime
    duration_minutes: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)