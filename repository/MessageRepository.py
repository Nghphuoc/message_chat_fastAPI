import datetime

from sqlalchemy import desc, asc
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
            skip: int = 0
            limit: int = 20
            messages = (
                self.db.query(Message)
                .filter(Message.room_id == room_id)
                .order_by(desc(Message.created_at))
                .offset(skip)
                .limit(limit)
                .all()
            )
            messages.reverse()
            return messages
        except Exception as e:
            raise Exception("ERROR GET MESSAGE", str(e))


    def delete_message_by_id(self, message_id: str):
        try:
            message = self.db.query(Message).filter(Message.message_id == message_id).first()
            if not message:
                raise Exception("Message not found")
            self.db.delete(message)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception("ERROR DELETE MESSAGE", str(e))


    def count_unread_messages(self, last_read: datetime, room_id: str) -> int:
        try:
            count = (
                self.db.query(Message)
                .filter(Message.room_id == room_id)
                .filter(Message.created_at > last_read)
                .count()
            )
            return count
        except Exception as e:
            print("ERROR COUNT UNREAD MESSAGE", str(e))
            raise Exception(str(e))