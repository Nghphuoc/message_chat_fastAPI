from fastapi import HTTPException

from model import ChatRoom
from model.schema import ChatRoomRequest, ChatRoomResponse
from repository import RoomRepository


class RoomService:


    def __init__(self, repo: RoomRepository):
        self.db = repo


    def insert_room(self, room: ChatRoomRequest) -> ChatRoomResponse:
        try:
            print("CREATE CHAT ROOM AT ROOM SERVICE")
            room_data = ChatRoom(name=room.name,
                                 is_group=room.is_group,
                                 created_at=room.created_at,
                                 created_by=room.created_by,)
            return self.db.create_room(room_data)
        except Exception as e:
            print("ERROR CREATE CHAT ROOM AT ROOM SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR CREATE CHAT ROOM SERVICE: " + str(e))


    def get_room_list(self)-> list[ChatRoomResponse]:
        try:
            print("GET ALL CHAT ROOM LIST SERVICE")
            room_data = self.db.get_all_rooms()
            # Convert SQLAlchemy models to ChatRoomResponse objects
            return [ChatRoomResponse.from_orm(room) for room in room_data]
        except Exception as e:
            print("ERROR GET ALL CHAT ROOM LIST SERVICE: " + str(e))
            raise HTTPException(status_code=404, detail="ERROR GET ALL CHAT ROOM LIST SERVICE: " + str(e))


    def get_room(self, room_id: str) -> ChatRoomResponse:
        try:
            print("GET CHAT ROOM AT ROOM SERVICE")
            room_data = self.db.get_room_id(room_id)
            return ChatRoomResponse.from_orm(room_data)
        except Exception as e:
            print("ERROR GET CHAT ROOM AT ROOM SERVICE: " + str(e))
            raise HTTPException(status_code=404, detail="ERROR GET CHAT ROOM SERVICE: " + str(e))


    def update_room(self,room_id: str, room: ChatRoomRequest) -> ChatRoomResponse:
        try:
            print("UPDATE CHAT ROOM AT ROOM SERVICE")
            # call get_room
            room_old = self.get_room(room_id)
            if room_old is not None:
                room_old.name = room.name
                self.db.update_room(room_old)
                return ChatRoomResponse.from_orm(room)
        except Exception as e:
            print("ERROR UPDATE CHAT ROOM AT ROOM SERVICE: " + str(e))
            raise HTTPException(status_code=404, detail="ERROR UPDATE CHAT ROOM SERVICE: " + str(e))

