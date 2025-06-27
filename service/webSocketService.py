import datetime

from cachetools import TTLCache

from model.schema import MessageRequest, UserResponse
from service import MessageService
from service.MessageService import to_vietnam_time
from service.UserService import UserService

"""
@author <PhuocHN>
@version <1.12>
@function_id none
"""
user_cache = TTLCache(maxsize=500, ttl=300)  # save max 500 user, sống 5 minute


class WebsocketService:


    async def get_user_info(self, data, service_user: UserService) -> UserResponse:
        if data in user_cache:
            return user_cache[data]
        data_user = service_user.get_user_by_id(data)
        user_cache[data] = data_user
        return data_user


    async def send_message(self, data, user_id, room_id, service_message: MessageService, service_user: UserService):
        data_send = MessageRequest(
        user=user_id,
        room=room_id,
        content=data["content"],
        file_url=data.get("file_url", ""),  # optional
        created_at=datetime.datetime.utcnow())
        try:
            # step 1: insert data message
            message_data = service_message.insert_message(data_send)
        except Exception as e:
            error_payload = {
                "type": "error",
                "data": {
                    "message": f"Lỗi xử lý message: {str(e)}"
                }
            }
            return error_payload
        # step 2: call cache get data user
        data_user = await self.get_user_info(user_id, service_user)
        if data_user.display_name is None:
            name_user = data_user.username
        else:
            name_user = data_user.display_name

        message_send = {
            "type": "message",
            "data": {
            "message_id": message_data.message_id,
            "user_id": user_id,
            "name_user": name_user,
            "img_url": data_user.img_url,
            "room_id": room_id,
            "content": data_send.content,
            "created_at": str(to_vietnam_time(data_send.created_at).isoformat())}
        }
        # step 3: send content
        return message_send