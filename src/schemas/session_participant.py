from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID





class ParticipantRead(BaseModel):
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)