from fastapi import HTTPException
from sqlalchemy import Boolean

from model import UserRoom
from model.schema import UserRoomResponse
from repository import UserRoomRepository

"""
@author <PhuocHN>
@version <1.12>
@function_id none
"""

class UserRoomService:

    def __init__(self, repo: UserRoomRepository):
        self.db = repo

    """
    create user room 
    @param user_id : str
    @param friend_id : str
    @param user_room_id : str
    """
    def create_user_room(self, user_id: str, friend_id: str, user_room_id: str) -> str:
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
            return friend_user_room.room_id
        except Exception as e:
            print("ERROR CREATE USER_ROOM AT USER ROOM SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})

    """
    get user room list ( all )
    @return: list[UserRoomResponse]
    """
    def get_user_room_list(self)-> list[UserRoomResponse]:
        try:
            print("GET USER ROOM LIST SERVICE")
            user_room_list = self.db.get_all_user_rooms()
            return [UserRoomResponse.from_orm(item) for item in user_room_list]
        except Exception as e:
            print("ERROR GET USER ROOM LIST SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})

    """
    get user room by id user
    @param user_id: str
    @return: list[UserRoomResponse]
    """
    def get_user_room_by_id(self, user_id: str) -> list[UserRoomResponse]:
        try:
            print("GET USER ROOM BY ID SERVICE")
            user_room_data = self.db.get_room_id_by_user(user_id)
            return [UserRoomResponse.from_orm(item) for item in user_room_data]
        except Exception as e:
            print("ERROR GET USER ROOM BY ID SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})


    """
    get all room of user
    @param user_id: str
    @return: list[str]
    """
    def get_all_list_room_for_user(self, user_id: str) -> list[str]:
        try:
            print("GET USER ROOM LIST SERVICE")
            user_room_list = self.db.get_all_room_for_user(user_id)
            return user_room_list
        except Exception as e:
            print("ERROR GET USER ROOM LIST SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})

    """
    get user id by room id
    @param room_id: str
    @return: list[UserRoomResponse]
    """
    def get_user_id_by_room_id(self, room_id: str) -> list[UserRoomResponse]:
        try:
            print("GET USER ROOM BY ID SERVICE")
            return self.db.get_user_by_room_id(room_id)
        except Exception as e:
            print("ERROR GET USER ROOM BY ID SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})

    """
    delete user room by room id
    @param room_id: str
    @return: bool
    """
    def delete_user_room_by_id(self, room_id: int) -> bool:
        try:
            print("DELETE USER ROOM BY ID SERVICE")
            self.db.delete_user_room(room_id)
            return True
        except Exception as e:
            print("ERROR DELETE USER ROOM BY ID SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})

    """
    update action check hidden or show room for user
    @param room_id: str
    @param user_id: str
    @param action_check: bool
    @return: bool
    """
    def update_action(self, room_id: str, user_id: str, action_check: bool) -> bool:
        try:
            print("UPDATE USER ROOM BY ID SERVICE")
            self.db.check_is_active(room_id, user_id, action_check)
            return True
        except Exception as e:
            print("ERROR UPDATE USER ROOM BY ID SERVICE: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})


    """
    update last_read_at check unread message user
    @param room_id: str
    @param user_id: str
    @return: bool
    """
    def update_last_read_at(self, room_id: str, user_id: str) -> bool:
        try:
            print("UPDATE LAST READ FOR USER ROOM")
            self.db.update_last_read(room_id, user_id)
            return True
        except Exception as e:
            print("ERROR UPDATE LAST READ FOR USER ROOM: ", str(e))
            raise HTTPException(status_code=404, detail={"message": e})