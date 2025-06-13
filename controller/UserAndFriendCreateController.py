
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from depends.dependecy import user_and_friend_service
from model.Friendship import TypeStatus
from service.UserAndFriendCreateService import UserAndFriendCreateService

router = APIRouter = APIRouter(prefix="/add_friend", tags=["Add Friend"])


@router.post("/add_friend/{friend_id}", status_code=status.HTTP_201_CREATED)
async def insert_friend(user_id: str,
                        friend_id: str,
                        service: UserAndFriendCreateService =
                        Depends(user_and_friend_service)):
    try:
        service.create_fiend_ship(user_id, friend_id)
        return {"message": " send request success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})


@router.put("/update_status/{friend_id}", status_code=status.HTTP_200_OK)
async def update_status_accept(user_id: str, friend_id: str ,status: TypeStatus,
                        service: UserAndFriendCreateService =
                        Depends(user_and_friend_service)):
    try:
        service.update_status_accept_friend(user_id, friend_id,status)
        return {"message": " Accept friend request success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})


@router.put("/update_reject/{friend_id}", status_code=status.HTTP_200_OK)
async def update_status_reject(user_id: str, friend_id: str ,status: TypeStatus,
                               service: UserAndFriendCreateService = Depends(user_and_friend_service)):
    try:
        service.update_status_reject_friend(user_id, friend_id,status)
        return {"message": f" reject friend request success {status}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})