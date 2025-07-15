from fastapi import HTTPException
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