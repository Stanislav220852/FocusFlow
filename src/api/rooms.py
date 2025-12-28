import uuid
from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.schemas.room import RoomRead,RoomCreate
from src.models.room import Room
from src.models.user import User
from src.api.dependencies import get_current_user

    
    
    
    
    
    
room_router = APIRouter(prefix="/rooms", tags=["Rooms"])



@room_router.post("/create_room",response_model=RoomRead)
async def create_room(
    data: RoomCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
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
