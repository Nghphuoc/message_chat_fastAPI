from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from depends.dependecy import user_service
from model.schema import UserRequest, UserResponse
from service import UserService

router: APIRouter= APIRouter(prefix="/api/user", tags=["User"])


@router.get("/all",status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_user_control(service: UserService = Depends(user_service)):
    try:
        return service.get_user()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("detail/{user_id}",status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_detail_user_control(user_id: str,service: UserService = Depends(user_service)):
    try:
        return service.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.post("/create",status_code=status.HTTP_202_ACCEPTED, response_model= UserResponse)
async def create_user_control(user: UserRequest ,service: UserService = Depends(user_service)):
    try:
        user_data = service.add_user(user)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.put("/update/{user_id}",status_code=status.HTTP_202_ACCEPTED, response_model=UserResponse)
async def update_user_control(user_id: str, user: UserRequest ,service: UserService = Depends(user_service)):
    try:
        user_data = service.update_user(user_id, user)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.delete("/delete/{user_id}",status_code=status.HTTP_202_ACCEPTED)
async def delete_user_control(user_id: str, service: UserService = Depends(user_service)):
    try:
        if service.delete_user_by_column(user_id):
            return {"message": "Delete success"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Error deleting user"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})