from fastapi import Depends
from sqlalchemy.orm import Session

from dbconfig.config import get_db
from repository.FriendRepository import FriendRepository
from repository.MessageRepository import MessageRepository
from repository.ReactionRepository import ReactionRepository
from repository.RoleRepository import RoleRepository
from repository.RoomRepository import RoomRepository
from repository.StatusRepository import StatusRepository
from repository.UserRepository import UserRepository
from repository.UserRoomRepository import UserRoomRepository
from service.FriendService import FriendService
from service.MessageService import MessageService
from service.ReactionService import ReactionService
from service.RoleService import RoleService
from service.RoomService import RoomService
from service.StatusService import StatusService
from service.UserAndFriendCreateService import UserAndFriendCreateService
from service.UserAndFriendService import UserAndFriendService
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


# user status service
def user_status_service(db: Session = Depends(get_db)):
    repo = StatusRepository(db)
    return StatusService(repo)


# room service
def room_service(db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    return RoomService(repo)


# user room service
def user_room_service(db: Session = Depends(get_db)):
    repo = UserRoomRepository(db)
    return UserRoomService(repo)


# friend service
def friend_service(db: Session = Depends(get_db)):
    repo = FriendRepository(db)
    return FriendService(repo)


# collab user and friend
def user_and_friend_service(db: Session = Depends(get_db)):
    chat_room = RoomRepository(db)
    chat_room_service = RoomService(chat_room)
    user_room_repo = UserRoomRepository(db)
    user_room_service = UserRoomService(user_room_repo)  # Important fix here
    friend = FriendRepository(db)
    friend_service = FriendService(friend)

    return UserAndFriendCreateService(chat_room_service, user_room_service, friend_service)


# message service
def message_service(db: Session = Depends(get_db)):
    repo = MessageRepository(db)
    reaction = ReactionRepository(db)
    return MessageService(repo, reaction)


# reaction service
def reaction_service(db: Session = Depends(get_db)):
    repo = ReactionRepository(db)
    return ReactionService(repo)

def user_friend_service(db: Session = Depends(get_db)):
    repo = StatusRepository(db)
    status = StatusService(repo)
    repo = RoleRepository(db)
    role =  RoleService(repo)
    user_repo = UserRepository(db)
    user_service = UserService(user_repo, role, status)
    friend = FriendRepository(db)
    friend_service = FriendService(friend)
    return UserAndFriendService(user_service, friend_service)