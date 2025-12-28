from typing import List
import uuid
from fastapi import APIRouter,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.schemas.room import RoomRead,RoomCreate
from src.models.room import Room
from src.models.user import User
from src.api.dependencies import get_current_user
from src.services.room_services import RoomService
from uuid import UUID
    
    
    
    
    
room_router = APIRouter(prefix="/rooms", tags=["Rooms"])



@room_router.post("/create_room",response_model=RoomRead)
async def create_room(
    data: RoomCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RoomService.create_new_room(db,data,current_user)
   

@room_router.get("/list_rooms",response_model=List[RoomRead])
async def list_rooms(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    return await RoomService.list_rooms(db, limit, offset)

@room_router.get("/{room_id}", response_model=RoomRead)
async def get_room(room_id: UUID, db: AsyncSession = Depends(get_db)):
    return await RoomService.get_room_by_id(db, room_id)



@room_router.delete("/{room_id}")
async def delete_room(
    room_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RoomService.delete_room(db, room_id, current_user.id)