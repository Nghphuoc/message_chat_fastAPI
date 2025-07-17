from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Boolean
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


@router.put("/update/action", status_code=status.HTTP_200_OK)
async def update_action_check(room_id: str, user_id: str, action_check: bool,
                              service: UserRoomService = Depends(user_room_service)):
    try:
        service.update_action(room_id, user_id, action_check)
        return {"message": "Action updated success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})