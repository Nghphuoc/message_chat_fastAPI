from fastapi import HTTPException

from model import UserRoom
from model.schema import UserRoomResponse
from repository import UserRoomRepository


class UserRoomService:

    def __init__(self, repo: UserRoomRepository):
        self.db = repo


    def create_user_room(self, user_id: str, friend_id: str, user_room_id: str) -> UserRoomResponse:
        try:
            print("CREATE USER ROOM AT ROOM SERVICE")
            new_user_room = UserRoom(
                user_id=user_id,
                room_id=user_room_id,
            )
            friend_user_room = UserRoom(
                user_id=friend_id,
                room_id=user_room_id,
            )
            self.db.create_user_room(new_user_room)
            self.db.create_user_room(friend_user_room)
            return friend_user_room
        except Exception as e:
            print("ERROR CREATE USER_ROOM AT USER ROOM SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail="USER_ROOM SERVICE NOT FOUND: " + str(e))


    def get_user_room_list(self)-> list[UserRoomResponse]:
        try:
            print("GET USER ROOM LIST SERVICE")
            user_room_list = self.db.get_all_user_rooms()
            return [UserRoomResponse.from_orm(list) for list in user_room_list]
        except Exception as e:
            print("ERROR GET USER ROOM LIST SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail="USER_ROOM SERVICE NOT FOUND: " + str(e))


    def get_user_room_by_id(self, room_id: int) -> UserRoomResponse:
        try:
            print("GET USER ROOM BY ID SERVICE")
            user_room_data = self.db.get_room_id_by_user(room_id)
            return UserRoomResponse.from_orm(user_room_data)
        except Exception as e:
            print("ERROR GET USER ROOM BY ID SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail="USER_ROOM SERVICE NOT FOUND: " + str(e))


    def delete_user_room_by_id(self, room_id: int) -> bool:
        try:
            print("DELETE USER ROOM BY ID SERVICE")
            self.db.delete_user_room(room_id)
            return True
        except Exception as e:
            print("ERROR DELETE USER ROOM BY ID SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail="USER_ROOM SERVICE NOT FOUND: " + str(e))