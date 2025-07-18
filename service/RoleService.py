from typing import List
from fastapi import HTTPException
from model import Role
from model.schema import RoleRequest, RoleResponse
from repository import RoleRepository
"""
@author <PhuocHN>
@version <1.12>
@function_id none
"""

class RoleService:


    def __init__(self, role_repo: RoleRepository):
        self.db = role_repo

    """
    get all role
    @return: list[RoleResponse] 
    """
    def get_roles(self) -> List[RoleResponse]:
        try:
            print("GET ALL ROLE AT SERVICE")
            roles = self.db.get_all_roles()
            # Convert SQLAlchemy models to RoleResponse objects
            return [RoleResponse.from_orm(role) for role in roles]
        except Exception as e:
            print("ERROR GET ALL ROLE AT SERVICE")
            raise HTTPException(status_code=500, detail={"message": e})

    """
    get role by role name
    @param: name : str
    @return: RoleResponse 
    """
    def get_role_by_role_name(self, name: str) -> RoleResponse:
        try:
            print("GET ROLE AT SERVICE")
            role = self.db.get_role_by_name(name)
            # Convert SQLAlchemy model to RoleResponse object
            return RoleResponse.from_orm(role)
        except Exception as e:
            print("ERROR GET ROLE AT SERVICE")
            raise HTTPException(status_code=404, detail={"message": e})

    """
    create new role
    @param: role : RoleRequest
    @return: RoleResponse 
    """
    def create_new_role(self, role: RoleRequest) -> RoleResponse:
        try:
            print("CREATE NEW ROLE AT SERVICE")
            role_new = Role(role_name=role.role_name)
            created_role = self.db.create_role(role_new)
            # Convert SQLAlchemy model to RoleResponse object
            return RoleResponse.from_orm(created_role)
        except Exception as e:
            print("ERROR CREATE NEW ROLE AT SERVICE:", str(e))
            raise HTTPException(status_code=400, detail={"message": e})

    """
    delete role by role_id
    @param: role_id : str
    @return: RoleResponse 
    """
    def delete_role(self, role_id: str) -> RoleResponse:
        try:
            print("DELETE ROLE AT SERVICE: ", role_id)
            return RoleResponse.from_orm(self.db.delete_role_by_role_id(role_id))
        except Exception as e:
            print("ERROR DELETE ROLE AT SERVICE:", str(e))
            raise HTTPException(status_code=404, detail={"message": e})
