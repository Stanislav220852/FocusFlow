from fastapi import APIRouter, Depends
from src.api.dependencies import get_current_user
from src.db.database import get_db
from src.services.focus_session_services import FocusSessionService
from src.schemas.focus_session import FocusSessionCreate, FocusSessionRead
from src.models.user import User
from uuid import UUID
from src.api.dependencies import DBSessionDep,CurrentUserDep

focus_router = APIRouter(prefix="/sessions", tags=["Sessions"])

@focus_router.post("/", response_model=FocusSessionRead)
async def start_session(
    data: FocusSessionCreate, 
    db: DBSessionDep, 
    user: CurrentUserDep
):
    return await FocusSessionService.start_session(db, data, user.id,data.room_id)

@focus_router.post("/{session_id}/join")
async def join_session(
    db: DBSessionDep,
    session_id: UUID, 
    user: CurrentUserDep
):
    return await FocusSessionService.join_session(db, session_id, user.id)