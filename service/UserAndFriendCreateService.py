import datetime as datetime

from fastapi import HTTPException

from model import ChatRoom, Friendship
from model.Friendship import TypeStatus
from model.schema import StatusRequest
from repository import UserAndFriendRepository
from service import FriendService
from service.RoomService import RoomService
from service.UserRoomService import UserRoomService

"""
@author <PhuocHN>
@version <1.12>
@function_id none
"""

class UserAndFriendCreateService:

    def __init__(self, chat_room: RoomService,
                 user_room: UserRoomService,
                 friend: FriendService, repo: UserAndFriendRepository ):
        self.chat_room = chat_room
        self.user_room = user_room
        self.friend = friend
        self.repo = repo

    """
    create friendship logic create ( room and update status friend )
    @:param user_id : str
    @param friend_id : str
    """
    def create_fiend_ship(self, user_id: str, friend_id: str):

        # check user friend
        data_user = self.friend.get_user_detail(user_id, friend_id)
        data_friend = self.friend.get_user_detail(friend_id, user_id)

        if data_friend is not None and data_user is not None:
            # call step 1: check already
            self.update_friend_request(data_user, data_friend)
        else:
            try:
                user = Friendship(
                    status=TypeStatus.WAIT,
                    created_at=datetime.datetime.now(),  # set here send request
                    friend_id=friend_id,
                    user_id=user_id,
                )

                # call to friend service create
                print("CREATE FIEND SHIP AT UserAndFriendCreateService ")
                self.friend.insert_friend_for_user(user)
            except Exception as e:
                print("ERROR CREATE FIEND SHIP AT UserAndFriendCreateService: " + str(e))
                raise HTTPException(status_code=500,
                                    detail={"message": e})


    """
    update status just use for accept friend
    @:param user_id : str
    @:param friend_id : str
    @:param status : TypeStatus
    """
    def update_status_accept_friend(self, user_id: str, friend_id: str, status: StatusRequest):
        try:
            print("UPDATE STATUS FRIEND AT UserAndFriendCreateService")
            self.friend.update_relationship_status(user_id, friend_id, status.status)

            try:
                room_data = ChatRoom(name="default",
                                     is_group=False,
                                     created_by=user_id)
                print("CREATE CHAT ROOM AT UserAndFriendCreateService")
                data_room = self.chat_room.insert_room(room_data)
            except Exception as e:
                print("ERROR CREATE CHAT ROOM AT UserAndFriendCreateService: " + str(e))
                raise HTTPException(status_code=500,
                                    detail={"message": e})
            try:
                print("CREATE USER ROOM AT UserAndFriendCreateService")
                self.user_room.create_user_room(user_id, friend_id, data_room.chat_room_id)
            except Exception as e:
                print("ERROR CREATE USER ROOM AT UserAndFriendCreateService: " + str(e))
                raise HTTPException(status_code=500,
                                    detail={"message": e})
        except Exception as e:
            print("ERROR UPDATE FRIEND AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400, detail={"message": e})


    """
    update status use reject friend ( cancel or block )
    @:param user_id : str
    @:param friend_id : str
    @:param status : TypeStatus
    """
    def update_status_reject_friend(self, user_id: str, friend_id: str, status: StatusRequest):
        try:
            print("UPDATE REJECT STATUS FRIEND AT UserAndFriendCreateService")
            self.friend.update_reject_status(user_id, friend_id, status.status)
        except Exception as e:
            print("ERROR UPDATE FRIEND AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400,
                                detail={"message": e})


    """
    update friend update when user cancel friend
    @:param data_user : Friendship
    @:param data_friend : Friendship
    """
    # step 1: check already
    def update_friend_request(self, data_user: Friendship, data_friend: Friendship):
        try:
            print("UPDATE FRIEND REQUEST CANCEL AT UserAndFriendCreateService")
            if data_user is None or data_friend is None:
                raise HTTPException(status_code=400,detail={"message": "Data User or Data Friend is None"})
            else:
                data_friend.status = TypeStatus.PENDING
                self.friend.update_status_request_again_status(data_friend)
                data_user.status = TypeStatus.WAIT
                self.friend.update_status_request_again_status(data_user)

        except Exception as e:
            print("ERROR UPDATE FRIEND REQUEST CANCEL AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400,
                                detail={"message": e})

    # # get list chat for user ( show img friend )
    # def get_list_user(self, ):


    """
    get list friend ( search input )
    @:param user_search_id : str
    @:param search_name: str
    @:return list
    """
    def search_user(self, user_search_id: str, search_name: str) -> list[dict]:
        try:
            print("SEARCH USER AT UserAndFriendCreateService")
            data_user = self.repo.search_users_with_status(user_search_id, search_name)
            return [self.serialize_user_result(row) for row in data_user]
        except Exception as e:
            print("ERROR SEARCH USER AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400,detail={"message": e})


    """
    parse to json 
    @:param row: str
    @:return dict
    """
    def serialize_user_result(self, row):
        return {
            "user_id": row.user_id,
            "display_name": row.display_name,
            "img_url": row.img_url,
            "friendship_status": row.friendship_status
        }
