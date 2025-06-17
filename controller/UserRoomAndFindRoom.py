from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status
from depends.dependecy import user_room_service, room_service, message_service
from model.schema import ChatRoomResponse, MessageResponse
from service import UserRoomService, RoomService, MessageService

router = APIRouter(prefix="/room/user", tags=["GetRoomForUser"])

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ChatRoomResponse])
async def get_all_room_of_user(user_id: str,
                               service_user_room: UserRoomService = Depends(user_room_service),
                               service_room: RoomService = Depends(room_service)
                               ):
    try:
        # step 1: call service at UserRoomService
        data = service_user_room.get_all_list_room_for_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
    try:
        # step 2: call service at RoomService
        list = []
        for room_tuple in data:
            room_id = room_tuple[0]
            chat_room = service_room.get_room(room_id)
            list.append(chat_room)
        return [ChatRoomResponse.from_orm(item) for item in list]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("/message", status_code=status.HTTP_200_OK, response_model=list[MessageResponse])
async def get_all_message(room_id: str, message_service: MessageService = Depends(message_service)):
    try:
        data = message_service.get_all_message_from_room(room_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})