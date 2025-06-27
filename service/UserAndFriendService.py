from fastapi import HTTPException
from service import UserService, FriendService

"""
@author <PhuocHN>
@version <1.12>
@function_id none
"""
class UserAndFriendService:

    def __init__(self, user: UserService, friend: FriendService):
        self.user = user
        self.friend = friend

    """
    get all request add friend
    @param: user_id : str
    return dict
    """
    def get_request_add_friend(self, user_id: str) -> list[dict]:
        try:
            friend = self.friend.get_request_friend(user_id)
            list = []
            for friend_data in friend:
                user_data = self.user.get_user_by_id(friend_data.friend_id)

                data = {
                    "user": user_data,
                    "status": friend_data.status,
                    "created_at": friend_data.created_at,
                }
                list.append(data)
            return list
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail={"message": e})
