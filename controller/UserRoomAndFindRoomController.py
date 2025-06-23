from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status
from depends.dependecy import user_room_service, room_service, message_service, user_service, user_status_service
from model.schema import ChatRoomResponse, MessageResponse, UserRoomResponse, UserInRoomResponse
from service import UserRoomService, RoomService, MessageService, UserService, StatusService
from service.MessageService import to_vietnam_time

router = APIRouter(prefix="/api/room/user", tags=["GetRoomForUser"])


@router.get("/list_chat/{user_id}", response_model=List[UserInRoomResponse], status_code=status.HTTP_200_OK)
async def get_all_room_of_user(user_id: str,
                               service_user_room: UserRoomService = Depends(user_room_service),
                               user_service: UserService = Depends(user_service),
                               user_status: StatusService = Depends(user_status_service)):

    try:
        room_ids = service_user_room.get_all_list_room_for_user(user_id)  # List of (room_id,)
        result = []
        name =""
        for room_tuple in room_ids:
            room_id = room_tuple[0]
            user_rooms = service_user_room.get_user_id_by_room_id(room_id)

            for user_room in user_rooms:
                if str(user_room.user_id) != str(user_id):
                    user_info = user_service.get_user_by_id(user_room.user_id)
                    # get status from user show with chat room call service
                    status_user = user_status.get_status_by_user(user_info.user_id)

                    if user_info.display_name:
                        name = user_info.display_name
                    else:
                        name = user_info.username

                    if user_info:  # đảm bảo tồn tại
                        result.append(UserInRoomResponse(
                            img_url=user_info.img_url,
                            username=name,
                            room_id=user_room.room_id,
                            status=status_user.is_online,
                            last_seen=to_vietnam_time(status_user.last_seen),
                        ))

        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("/message", status_code=status.HTTP_200_OK, response_model=list[MessageResponse])
async def get_all_message(room_id: str, message_service: MessageService = Depends(message_service)):
    try:
        data = message_service.get_all_message_from_room(room_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})