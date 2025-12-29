import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base  
from uuid import UUID
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.room import Room
    from src.models.session_participant import SessionParticipant

class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean,default=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    duration_minutes:Mapped[int] = mapped_column(Integer,default= 25)
    room: Mapped["Room"] = relationship(back_populates="sessions")
    participants: Mapped[List["SessionParticipant"]] = relationship(back_populates="session")