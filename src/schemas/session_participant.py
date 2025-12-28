from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID







class ParticipantRead(BaseModel):
    user_id: UUID
    earned_xp: int

    model_config = ConfigDict(from_attributes=True)