import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.focus_session import FocusSession
from models.user import User
from src.db.database import Base  
from uuid import UUID


class SessionParticipant(Base):
    __tablename__ = "session_participants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[UUID] = mapped_column(ForeignKey("focus_sessions.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    earned_xp: Mapped[int] = mapped_column(Integer, default=0)
    session: Mapped["FocusSession"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="session_history")