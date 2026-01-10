from fastapi import APIRouter, Depends
from src.api.dependencies import get_current_user
from src.db.database import get_db
from src.services.focus_session_services import FocusSessionService
from src.schemas.focus_session import FocusSessionCreate, FocusSessionRead
from src.models.user import User
from uuid import UUID
from src.api.dependencies import DBSessionDep,CurrentUserDep,RedisDep


focus_router = APIRouter(prefix="/sessions", tags=["Sessions"])

@focus_router.post("/start", response_model=FocusSessionRead)
async def start_session(
    data: FocusSessionCreate, 
    db: DBSessionDep, 
    cache:RedisDep,
    user: CurrentUserDep
):
    return await FocusSessionService.start_session(data,db,cache, user.id)

@focus_router.post("/{session_id}/join")
async def join_session(
    db: DBSessionDep,
    session_id: UUID, 
    user: CurrentUserDep
):
    return await FocusSessionService.join_session(db, session_id, user.id)    


@focus_router.get("/{session_id}/remaining")
async def get_remaining_time(
    session_id: UUID,
    cache: RedisDep 
):
    
    ttl = await cache.ttl(f"session:{session_id}:timer")
    
    if ttl == -2:
        return {"is_active": False, "remaining_seconds": 0}
    
    return {
        "is_active": True,
        "remaining_seconds": ttl,
        "minutes": ttl // 60,
        "seconds": ttl % 60
    }