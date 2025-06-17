from fastapi import HTTPException

from model import Message
from model.schema import MessageRequest, MessageResponse
from repository import MessageRepository


class MessageService:

    def __init__(self, repo: MessageRepository):
        self.db = repo


    def insert_message(self, message: MessageRequest)-> MessageResponse:
        try:
            print("CREATE MESSAGE AT MessageService")
            message_data = Message(
                content=message.content,
                file_url=message.file_url,
                created_at=message.created_at,
                room_id=message.room,
                user_id=message.user,
            )
            data_message = self.db.create_message(message_data)
            return MessageResponse.from_orm(data_message)
        except Exception as e:
            print("ERROR CREATE MESSAGE AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR CREATE MESSAGE AT MessageService: " + str(e))


    def get_message(self) -> list[MessageResponse]:
        try:
            print("GET MESSAGE AT MessageService")
            data_message = self.db.get_message_all()
            return [MessageResponse.from_orm(list) for list in data_message]
        except Exception as e:
            print("ERROR CREATE MESSAGE AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR CREATE MESSAGE AT MessageService: " + str(e))


    # get all message from room_id
    def get_all_message_from_room(self, room_id: str) -> list[MessageResponse]:
        try:
            print("GET ALL MESSAGE FROM ROOM AT MessageService")
            data_message = self.db.get_message_from_room_id(room_id)
            return [MessageResponse.from_orm(list) for list in data_message]
        except Exception as e:
            print("ERROR GET ALL MESSAGE FROM ROOM AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR ALL MESSAGE FROM ROOM AT MessageService: " + str(e))