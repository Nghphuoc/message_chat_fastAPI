from sqlalchemy import desc
from sqlalchemy.orm import Session

from model import Message


class MessageRepository:


    def __init__(self, session: Session):
        self.db = session


    def create_message(self, message: Message):
        try:
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            return message
        except Exception as e:
            self.db.rollback()
            raise Exception("ERROR CREATE MESSAGE", str(e))


    def get_message_all(self):
        try:
            messages = self.db.query(Message).all()
            return messages
        except Exception as e:
            self.db.rollback()
            raise Exception("ERROR GET MESSAGE", str(e))


    def get_message_from_room_id(self, room_id: str):
        try:
            messages = (
                self.db.query(Message)
                .filter(Message.room_id == room_id)
                .order_by(desc(Message.created_at))
                .all()
            )
            return messages
        except Exception as e:
            raise Exception("ERROR GET MESSAGE", str(e))
