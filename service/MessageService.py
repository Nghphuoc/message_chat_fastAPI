import datetime
from fastapi import HTTPException
import pytz
from model import Message
from model.schema import MessageRequest, MessageResponse
from repository import MessageRepository, ReactionRepository

"""
@author: PhuocHN
@version: 1.12
@function_id: none
"""

class MessageService:

    def __init__(self, repo: MessageRepository, reaction: ReactionRepository):
        self.db = repo
        self.reaction = reaction

    """
    create new message
    @param: message : MessageRequest
    @return: MessageResponse
    """
    def insert_message(self, message: MessageRequest)-> MessageResponse:
        try:
            print("CREATE MESSAGE AT MessageService")
            message_data = Message(
                content=message.content,
                file_url=message.file_url,
                created_at=message.created_at,
                room_id=message.room,
                user_id=message.user,
                reply_to_message_id=message.reply_to_message_id or None,
            )
            data_message = self.db.create_message(message_data)
            return MessageResponse.from_orm(data_message)
        except Exception as e:
            print("ERROR CREATE MESSAGE AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR CREATE MESSAGE AT MessageService: " + str(e))

    """
    get all message
    @:param none
    @:return: MessageResponse 
    """
    def get_message(self) -> list[MessageResponse]:
        try:
            print("GET MESSAGE AT MessageService")
            data_message = self.db.get_message_all()
            return [MessageResponse.from_orm(list) for list in data_message]
        except Exception as e:
            print("ERROR CREATE MESSAGE AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR CREATE MESSAGE AT MessageService: " + str(e))


    """
    get all message from room_id
    @:param room_id : str
    @:return: dict
    """
    def get_all_message_from_room(self,skip: int, room_id: str) -> list[dict]:
        try:
            print("GET ALL MESSAGE FROM ROOM AT MessageService")
            data_messages = self.db.get_message_from_room_id(skip, room_id)  # Assume this returns ORM objects or dict-like

            # Convert each message into the desired dictionary format
            result = []
            for message_data in data_messages:

                reaction = self.reaction.get_reaction_by_message_id(message_data.message_id)

                user_id = message_data.user.user_id
                name_user = message_data.user.username
                img_url = message_data.user.img_url  # or message_data.user.img_url depending on your model
                content = message_data.content
                created_at = str(to_vietnam_time(message_data.created_at))

                message_dict = {
                    "message_id": message_data.message_id,
                    "user_id": user_id,
                    "name_user": name_user,
                    "img_url": img_url,
                    "room_id": room_id,
                    "content": content,
                    "created_at": created_at,
                    "icon": reaction,
                    "reply": {
                        "message_id": message_data.reply_to.message_id,
                        "user_id": message_data.reply_to.user.user_id,
                        "name_user": message_data.reply_to.user.username,
                        "content": message_data.reply_to.content,
                    } if message_data.reply_to else None
                }
                result.append(message_dict)

            return result

        except Exception as e:
            print("ERROR GET ALL MESSAGE FROM ROOM AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="ERROR ALL MESSAGE FROM ROOM AT MessageService: " + str(e))


    def delete_message(self, message_id: str):
        try:
            print("DELETE MESSAGE AT MessageService")
            return self.db.delete_message_by_id(message_id)
        except Exception as e:
            print("ERROR DELETE MESSAGE AT MessageService: " + str(e))
            raise HTTPException(status_code=500, detail="message: " + str(e))


"""
parse time global to vietnam_time GMT +7
@param: utc_dt : datetime
@return: datetime
"""
def to_vietnam_time( utc_dt: datetime) -> datetime:
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=datetime.timezone.utc)
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return utc_dt.astimezone(vn_tz)