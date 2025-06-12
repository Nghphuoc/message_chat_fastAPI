from sqlalchemy import desc
from sqlalchemy.orm import Session

from model import ChatRoom


class RoomRepository:


    def __init__(self, session: Session):
        self.db = session


    def create_room(self, chat_room: ChatRoom):
        try:
            self.db.add(chat_room)
            self.db.commit()
            self.db.refresh(chat_room)
            return chat_room
        except Exception as e:
            print("ERROR CREATE CHAT ROOMS: " + str(e))
            raise Exception("ERROR CREATE CHAT ROOMS: " + str(e))


    def get_room_id(self, chat_room_id: str):
        try:
            return self.db.query(ChatRoom).filter(ChatRoom.chat_room_id == chat_room_id).first()
        except Exception as e:
            print("ERROR GET CHAT ROOMS: " + str(e))
            raise Exception("ERROR GET CHAT ROOMS: " + str(e))


    def get_all_rooms(self):
        try:
            return self.db.query(ChatRoom).order_by(desc(ChatRoom.created_at)).all()
        except Exception as e:
            print("ERROR GET CHAT ROOMS: " + str(e))
            raise Exception("ERROR GET CHAT ROOMS: " + str(e))


    # def get_room_by_name_for_user(self, user_id: str, chat_room_id: str):
    #     try:
    #         return self.db.query(ChatRoom).filter()


    def delete_room_by_id(self, chat_room_id: str):
        try:
            self.db.query(ChatRoom).filter(ChatRoom.id == chat_room_id).delete()
            self.db.commit()
            self.db.refresh(chat_room_id)
            return True
        except Exception as e:
            print("ERROR DELETE CHAT ROOMS: " + str(e))
            raise Exception("ERROR DELETE CHAT ROOMS: " + str(e))