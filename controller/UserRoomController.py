from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from depends.dependecy import user_room_service
from model.schema import UserRoomResponse
from service import UserRoomService

router = APIRouter = APIRouter(prefix="/api/user_room", tags=["UserRoom"])


@router.get("/all", response_model=List[UserRoomResponse], status_code=status.HTTP_200_OK)
async def get_all_user_rooms(service: UserRoomService = Depends(user_room_service)):
    try:
        return service.get_user_room_list()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("/detail/{user_id}", response_model=list[UserRoomResponse], status_code=status.HTTP_200_OK)
async def get_user_room(user_id: str, service: UserRoomService = Depends(user_room_service)):
    try:
        return service.get_user_room_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.delete("/delete/{room_id}", response_model=UserRoomResponse, status_code=status.HTTP_200_OK)
async def delete_user_room(room_id: str, service: UserRoomService = Depends(user_room_service)):
    try:
        return service.delete_user_room_by_id(room_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
