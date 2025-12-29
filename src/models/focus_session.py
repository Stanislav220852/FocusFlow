import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base

if TYPE_CHECKING:
    from src.models.room import Room
    from src.models.session_participant import SessionParticipant

class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    
    duration_minutes: Mapped[int] = mapped_column(default=25)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Relationships
    room: Mapped["Room"] = relationship(back_populates="sessions")
    participants: Mapped[List["SessionParticipant"]] = relationship(back_populates="session")