from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status
from depends.dependecy import room_service
from model.schema import ChatRoomResponse, ChatRoomRequest
from service import RoomService

router = APIRouter = APIRouter(prefix="/api/room", tags=["Room"])

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ChatRoomResponse])
async def get_all_rooms(service: RoomService = Depends(room_service)):
    try:
        return service.get_room_list()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/detail/{room_id}", status_code=status.HTTP_200_OK, response_model=ChatRoomResponse)
async def get_room(room_id: str, service: RoomService = Depends(room_service)):
    try:
        return service.get_room(room_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ChatRoomResponse)
async def create_room(room: ChatRoomRequest, service: RoomService = Depends(room_service)):
    try:
        return service.insert_room(room)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update/{room_id}", status_code=status.HTTP_200_OK, response_model=ChatRoomResponse)
async def update(room_id: str, service: RoomService = Depends(room_service)):
    try:
        return service.update_room(room_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))