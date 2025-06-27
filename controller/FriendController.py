from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from depends.dependecy import friend_service, user_friend_service
from model.schema import FriendResponse
from service import FriendService
from service.UserAndFriendService import UserAndFriendService

router = APIRouter = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("/list_friends/{user_id}", response_model=list[FriendResponse], status_code=status.HTTP_200_OK)
async def list_friends(user_id: str, service: FriendService = Depends(friend_service)):
    try:
        return service.get_friend_list(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.delete("/delete_friends/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_friend(friend_id: str, user_id: str, service: FriendService = Depends(friend_service)):
    try:
        return service.delete_friend_for_user(user_id, friend_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("/request", response_model=list[FriendResponse], status_code=status.HTTP_201_CREATED)
async def request_friend(user_id: str, service: FriendService = Depends(friend_service)):
    try:
        return service.get_request_friend(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("/detail/request/{user_id}", response_model=list[dict], status_code=status.HTTP_200_OK)
async def request_detail(user_id: str, service: UserAndFriendService = Depends(user_friend_service)):
    try:
        return service.get_request_add_friend(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
