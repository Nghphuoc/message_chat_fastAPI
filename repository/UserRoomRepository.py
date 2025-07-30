import datetime

from sqlalchemy import desc, Boolean, update
from sqlalchemy.orm import Session
from sqlalchemy.testing import db

from model import UserRoom


class UserRoomRepository:


    def __init__(self, session: Session):
        self.db = session


    def create_user_room(self, user_room: UserRoom):
        try:
            self.db.add(user_room)
            self.db.commit()
            self.db.refresh(user_room)
            return user_room
        except Exception as e:
            self.db.rollback()
            raise Exception("Error while creating user room: " + str(e))


    def get_all_user_rooms(self):
        try:
            return self.db.query(UserRoom).order_by(desc(UserRoom.joined_at)).all()
        except Exception as e:
            self.db.rollback()
            raise Exception("Error while getting all user rooms: " + str(e))


    # get all room of user
    def get_all_room_for_user(self, user_id: str) -> list[str]:
        try:
            return self.db.query(UserRoom.room_id).filter(UserRoom.user_id == user_id).all()
        except Exception as e:
            self.db.rollback()
            raise Exception("Error while getting all rooms for user: " + str(e))


    # get list chatroom id
    def get_room_id_by_user(self, user_id: str):
        try:
            return self.db.query(UserRoom).filter(UserRoom.user_id == user_id).all()
        except Exception as e:
            self.db.rollback()
            raise Exception("Error while getting user room: " + str(e))


    def get_user_by_room_id(self, room_id: str):
        try:
            return self.db.query(UserRoom).filter(UserRoom.room_id == room_id).all()
        except Exception as e:
            self.db.rollback()
            raise Exception("Error while getting user room: " + str(e))


    def delete_user_room(self, user_room_id: str):
        try:
            self.db.query(UserRoom).filter(UserRoom.user_id == user_room_id).delete()
            self.db.commit()
            self.db.refresh(UserRoom)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception("Error while deleting user room: " + str(e))


    def check_is_active(self, room_id: str, user_id: str, action_check: bool)-> bool:
        try:
            (self.db.query(UserRoom).filter(UserRoom.room_id == room_id)
             .filter(UserRoom.user_id == user_id).update({UserRoom.is_active: action_check}))
            self.db.commit()
            return True
        except Exception as e:
            print("Error while checking if user room is active: " + str(e))
            self.db.rollback()
            raise Exception(str(e))


    def update_last_read(self, room_id: str, user_id: str):
        try:
            (self.db.query(UserRoom).filter(UserRoom.room_id == room_id)
             .filter(UserRoom.user_id == user_id)).update({UserRoom.last_read_at: datetime.datetime.now()})
            self.db.commit()
        except Exception as e:
            print("Error while updating last read: " + str(e))
            self.db.rollback()
            raise Exception(str(e))