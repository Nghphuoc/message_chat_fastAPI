from fastapi import Depends
from sqlalchemy.orm import Session

from dbconfig.config import get_db
from repository.FriendRepository import FriendRepository
from repository.MessageRepository import MessageRepository
from repository.RoleRepository import RoleRepository
from repository.RoomRepository import RoomRepository
from repository.StatusRepository import StatusRepository
from repository.UserRepository import UserRepository
from repository.UserRoomRepository import UserRoomRepository
from service.FriendService import FriendService
from service.MessageService import MessageService
from service.RoleService import RoleService
from service.RoomService import RoomService
from service.StatusService import StatusService
from service.UserAndFriendCreateService import UserAndFriendCreateService
from service.UserRoomService import UserRoomService
from service.UserService import UserService


# user service
def user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)

    role_repo = RoleRepository(db)
    role = RoleService(role_repo)

    status_repo = StatusRepository(db)
    status = StatusService(status_repo)

    return UserService(repo, role, status)


# role service
def role_service(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    return RoleService(repo)


def user_status_service(db: Session = Depends(get_db)):
    repo = StatusRepository(db)
    return StatusService(repo)


def room_service(db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    return RoomService(repo)


def user_room_service(db: Session = Depends(get_db)):
    repo = UserRoomRepository(db)
    return UserRoomService(repo)


def friend_service(db: Session = Depends(get_db)):
    repo = FriendRepository(db)
    return FriendService(repo)


def user_and_friend_service(db: Session = Depends(get_db)):
    chat_room = RoomRepository(db)
    chat_room_service = RoomService(chat_room)
    user_room_repo = UserRoomRepository(db)
    user_room_service = UserRoomService(user_room_repo)  # Important fix here
    friend = FriendRepository(db)
    friend_service = FriendService(friend)

    return UserAndFriendCreateService(chat_room_service, user_room_service, friend_service)


def message_service(db: Session = Depends(get_db)):
    repo = MessageRepository(db)
    return MessageService(repo)
