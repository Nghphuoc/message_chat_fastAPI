import datetime as datetime

from fastapi import HTTPException

from model import ChatRoom, Friendship
from model.Friendship import TypeStatus
from service import FriendService
from service.RoomService import RoomService
from service.UserRoomService import UserRoomService


class UserAndFriendCreateService:

    def __init__(self, chat_room: RoomService, user_room: UserRoomService ,friend: FriendService):
        self.chat_room = chat_room
        self.user_room = user_room
        self.friend = friend


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
                                    detail="ERROR CREATE FIEND SHIP AT UserAndFriendCreateService: " + str(e))

            try:
                room_data = ChatRoom(name="default",
                                     is_group=False,
                                     created_by=user_id, )
                # call create room chat
                print("CREATE CHAT ROOM AT UserAndFriendCreateService")
                data_room = self.chat_room.insert_room(room_data)
            except Exception as e:
                print("ERROR CREATE CHAT ROOM AT UserAndFriendCreateService: " + str(e))
                raise HTTPException(status_code=500,
                                    detail="ERROR CREATE ROOM AT UserAndFriendCreateService: " + str(e))

            try:
                # call user room service
                print("CREATE USER ROOM AT UserAndFriendCreateService")
                self.user_room.create_user_room(user_id, friend_id, data_room.chat_room_id)
            except Exception as e:
                print("ERROR CREATE USER ROOM AT UserAndFriendCreateService: " + str(e))
                raise HTTPException(status_code=500,
                                    detail="ERROR CREATE ROOM AT UserAndFriendCreateService: " + str(e))


    # just use for accept friend
    def update_status_accept_friend(self, user_id: str, friend_id: str, status: TypeStatus):
        try:
            print("UPDATE STATUS FRIEND AT UserAndFriendCreateService")
            self.friend.update_relationship_status(user_id, friend_id, status)
        except Exception as e:
            print("ERROR UPDATE FRIEND AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400, detail="ERROR UPDATE FRIEND AT UserAndFriendCreateService: " + str(e))


    # use reject friend
    def update_status_reject_friend(self, user_id: str, friend_id: str, status: TypeStatus):
        try:
            print("UPDATE REJECT STATUS FRIEND AT UserAndFriendCreateService")
            self.friend.update_reject_status(user_id, friend_id, status)
        except Exception as e:
            print("ERROR UPDATE FRIEND AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400,
                                detail="ERROR UPDATE REJECT FRIEND AT UserAndFriendCreateService: " + str(e))


    # update when user cancel friend
    # step 1: check already
    def update_friend_request(self, data_user: Friendship, data_friend: Friendship):
        try:
            print("UPDATE FRIEND REQUEST CANCEL AT UserAndFriendCreateService")
            if data_user is not None:
                data_user.status = TypeStatus.WAIT
                self.friend.update_status_request_again_status(data_user)

            if data_friend is not None:
                data_friend.status = TypeStatus.PENDING
                self.friend.update_status_request_again_status(data_friend)

        except Exception as e:
            print("ERROR UPDATE FRIEND REQUEST CANCEL AT UserAndFriendCreateService: " + str(e))
            raise HTTPException(status_code=400,
                                detail={"message": "UPDATE FRIEND REQUEST CANCEL AT UserAndFriendCreateService: " + str(e)})

    # # get list chat for user ( show img friend )
    # def get_list_user(self, ):