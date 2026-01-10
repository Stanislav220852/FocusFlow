from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends,status
from src.models.user import User
from src.schemas.room import RoomCreate
from src.models.room import Room
from src.api.dependencies import get_current_user
from uuid import UUID
import uuid






class RoomService:
    @staticmethod
    async def create_new_room(db:AsyncSession,data: RoomCreate,current_user: User = Depends(get_current_user)):
        new_room = Room(
            name = data.name,
            description = data.description,
            work_duration = data.work_duration,
            break_duration = data.break_duration,
            is_private = data.is_private,
            creator_id= current_user.id 
        )
        if data.is_private:
            new_room.invite_code = uuid.uuid4().hex[:8].upper()
    
        db.add(new_room)
        await db.commit()
        await db.refresh(new_room)
        return new_room
        
    @staticmethod
    async def list_rooms(db: AsyncSession, limit: int = 20, offset: int = 0):
       
        query = (
            select(Room)
            .where(Room.is_private == False)
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    
    @staticmethod
    async def get_room_by_id(db: AsyncSession, room_id: UUID):
        
        query = select(Room).where(Room.id == room_id)
        result = await db.execute(query)
        room = result.scalar_one_or_none()
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        return room

    
    @staticmethod
    async def delete_room(db: AsyncSession, room_id: UUID, user_id: UUID):
       
        room = await RoomService.get_room_by_id(db, room_id)
        
        
        if room.creator_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this room"
            )
        
        await db.delete(room)
        await db.commit()
        return {"detail": "Room deleted successfully"}