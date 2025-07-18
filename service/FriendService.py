from typing import List
from fastapi import HTTPException
from model import Friendship
from model.Friendship import TypeStatus
from model.schema import FriendRequest, FriendResponse
from repository import FriendRepository

""" 
@author: <PhuocHN>
@version: <1.12>
@function_id: none
"""

class FriendService:

    def __init__(self, repo: FriendRepository):
        self.db = repo

    """
    create new relationship friend ( sent request add friend )
    @param: friend : FriendRequest
    @return: True
    """
    def insert_friend_for_user(self, friend: FriendRequest):
        try:
            print("CREATE FIEND AT FRIEND SERVICE")
            user = Friendship(
                status=TypeStatus.WAIT, # set here send request
                created_at=friend.created_at,
                friend_id=friend.friend_id,
                user_id=friend.user_id,
            )

            friend = Friendship(
                status=TypeStatus.PENDING,
                created_at=friend.created_at,
                friend_id=friend.user_id,
                user_id=friend.friend_id,
            )
            self.db.create_friend(user)
            self.db.create_friend(friend)
            return True
        except Exception as e:
            print("ERROR CREATE FRIEND AT FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e})

    """
    get detail friendship of user
    @param: user_id : str
    @param: friend_id : str
    @return: Friendship
    """
    def get_user_detail(self, user_id: str, friend_id: str)->FriendRequest:
        try:
            print("GET DETAIL USER FIEND AT FRIEND SERVICE")
            return self.db.get_detail_user(user_id, friend_id)
        except Exception as e:
            print("ERROR GET DETAIL USER FIEND SERVICE: " + str(e))
            raise HTTPException(status_code=404, detail={"message": e})


    """
    create new relationship friend ( sent request custom friend )
    @param: friend : FriendRequest
    @return: 
    """
    def create_user_not_status(self, friend: FriendRequest):
        try:
            print("CREATE FIEND AT FRIEND SERVICE")
            user = Friendship(
                status=friend.status,
                created_at=friend.created_at,
                friend_id=friend.user_id,
                user_id=friend.friend_id,
            )
            self.db.create_friend(user)
        except Exception as e:
            print("ERROR CREATE FRIEND AT FRIEND SERVICE: " + str(e))
        raise HTTPException(status_code=500, detail={"message": e})

    """
    get list friend of user
    @param: user_id : str
    @return: FriendshipResponse
    """
    def get_friend_list(self, user_id: str)->List[FriendResponse]:
        try:
            print("GET ALL FIEND AT FRIEND SERVICE")
            friend_list = self.db.get_friends_by_user_id(user_id)
            return [FriendResponse.from_orm(list) for list in friend_list]
        except Exception as e:
            print("ERROR GET ALL FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e})

    """
    delete friend of user
    @param: user_id : str
    @param: friend_id : str
    @return: True
    """
    def delete_friend_for_user(self, user_id: str, friend_id: str):
        try:
            print("DELETE FIEND AT FRIEND SERVICE")
            self.db.delete_friend_relationship(user_id, friend_id)
            return True
        except Exception as e:
            print("ERROR DELETE FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e})


    """
    update friend status of user ( just use for accept friend )
    @param: user_id : str
    @param: friend_id : str
    @param: status : TypeStatus
    @return: True
    """
    def update_relationship_status(self, user_id: str, friend_id: str, status: TypeStatus):
        try:
            print("UPDATE STATUS FIEND AT FRIEND SERVICE")
            update_status_user = self.db.get_friend_relationship(user_id, friend_id)
            if update_status_user is not None:
                update_status_user.status = status
                self.db.create_friend(update_status_user)

            update_status_friend = self.db.get_friend_relationship(friend_id, user_id)
            if update_status_friend is not None:
                update_status_friend.status = status
                self.db.create_friend(update_status_friend)
                return True
            return None
        except Exception as e:
            print("ERROR UPDATE STATUS FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e })


    """
    use other update status friend ( allow user block or cancel fiend )
    @param: user_id : str
    @param: friend_id : str
    @param: status : TypeStatus
    @return: True
    """
    def update_reject_status(self, user_id: str, friend_id: str, status: TypeStatus):
        try:
            print("UPDATE REJECT STATUS FIEND AT FRIEND SERVICE")
            update_status_user = self.db.get_friend_relationship(user_id, friend_id)
            if update_status_user is not None:
                update_status_user.status = status
                self.db.create_friend(update_status_user)
            return True
        except Exception as e:
            print("ERROR REJECT UPDATE STATUS FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e })


    """
    update request status ( add friend when friend cancel )
    @param: friend : FriendRequest
    @return: True
    """
    def update_status_request_again_status(self, friend: FriendRequest):
        try:
            print("UPDATE STATUS FIEND AT FRIEND SERVICE")
            self.db.update_friend_status(friend)
            return True
        except Exception as e:
            print("ERROR UPDATE STATUS FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e })


    """
    get all request add friend
    @param: user_id : str
    return FriendshipResponse
    get_request_add_friend
    """
    def get_request_friend(self, user_id: str)->List[FriendResponse]:
        try:
            print("GET ALL FIEND AT FRIEND SERVICE")
            friend_list = self.db.get_request_add_friend(user_id)
            return [FriendResponse.from_orm(list) for list in friend_list]
        except Exception as e:
            print("ERROR GET ALL FRIEND SERVICE: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e})