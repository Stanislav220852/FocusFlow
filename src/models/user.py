import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base

if TYPE_CHECKING:
    from src.models.room import Room
    from src.models.session_participant import SessionParticipant

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    xp: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=1)
    total_minutes_focused: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    created_rooms: Mapped[List["Room"]] = relationship(back_populates="creator")
    session_history: Mapped[List["SessionParticipant"]] = relationship(back_populates="user")


