import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.focus_session import FocusSession

class SessionParticipant(Base):
    __tablename__ = "session_participants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("focus_sessions.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    earned_xp: Mapped[int] = mapped_column(default=0)

    # Relationships
    session: Mapped["FocusSession"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="session_history")