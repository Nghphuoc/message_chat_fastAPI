from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from depends.dependecy import role_service
from model.schema import RoleResponse, RoleRequest
from service import RoleService

router: APIRouter = APIRouter(prefix="/api/role", tags=["Role"])


@router.get("/all", response_model=List[RoleResponse], status_code=status.HTTP_200_OK)
async def get_role(service: RoleService = Depends(role_service)):
    try:
        return service.get_roles()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.get("/{role_name}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
async def get_role_by_name(role_name: str ,service: RoleService = Depends(role_service)):
    try:
        return service.get_role_by_role_name(role_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.post("/create", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleRequest, service: RoleService = Depends(role_service)):
    try:
        return service.create_new_role(role)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})


@router.delete("/delete/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
async def delete_role_by_id(role_id: str, service: RoleService = Depends(role_service)):
    try:
        return service.delete_role(role_id=role_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})