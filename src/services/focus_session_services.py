from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models.focus_session import FocusSession
from src.schemas.focus_session import FocusSessionCreate
from src.models.room import Room
from src.services.room_services import RoomService
from uuid import UUID
from src.models.session_participant import SessionParticipant
from src.api.dependencies import RedisDep



class FocusSessionService:
    @staticmethod
    async def start_session(data: FocusSessionCreate,db: AsyncSession,  cache: RedisDep, user_id: int):
        
        room = await RoomService.get_room_by_id(db, data.room_id)
        if not room or room.creator_id != user_id:
            raise HTTPException(status_code=403, detail="Только владелец может запустить фокус")

        
        query = select(FocusSession).where(
            and_(FocusSession.room_id == data.room_id, FocusSession.is_active == True)
        )
        existing = await db.execute(query)
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Сессия в этой комнате уже идет")

       
        new_session = FocusSession(**data.model_dump())
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        
        redis_key = f"session:{new_session.id}:timer"
        await cache.set(redis_key, "active", ex=data.duration_minutes * 60)
        return new_session
    
    
    @staticmethod
    async def join_session(db: AsyncSession, session_id: int, user_id: int):
        # Проверяем сессию
        session = await db.get(FocusSession, session_id)
        if not session or not session.is_active:
            raise HTTPException(status_code=400, detail="Сессия не активна")

        
        participant = SessionParticipant(session_id=session_id, user_id=user_id)
        db.add(participant)
        await db.commit()
        return {"message": "Вы присоединились к фокусу"}