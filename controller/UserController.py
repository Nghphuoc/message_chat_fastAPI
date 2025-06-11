from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from depends.dependecy import user_service
from model.schema import UserRequest, UserResponse
from service import UserService

router: APIRouter= APIRouter(prefix="/api/user", tags=["User"])


@router.get("/all",status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_user(service: UserService = Depends(user_service)):
    try:
        return service.get_user()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.post("/create",status_code=status.HTTP_202_ACCEPTED, response_model= UserResponse)
async def post_user(user: UserRequest ,service: UserService = Depends(user_service)):
    try:
        user_data = service.add_user(user)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})