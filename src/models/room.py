import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.focus_session import FocusSession

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    
    creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    work_duration: Mapped[int] = mapped_column(default=25)
    break_duration: Mapped[int] = mapped_column(default=5)
    is_private: Mapped[bool] = mapped_column(default=False)
    invite_code: Mapped[Optional[str]] = mapped_column(String(10), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    creator: Mapped["User"] = relationship(back_populates="created_rooms")
    sessions: Mapped[List["FocusSession"]] = relationship(back_populates="room")