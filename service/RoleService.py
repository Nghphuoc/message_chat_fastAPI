from typing import List
from fastapi import HTTPException
from model import Role
from model.Role import RoleType
from model.schema import RoleRequest, RoleResponse
from repository import RoleRepository


class RoleService:


    def __init__(self, role_repo: RoleRepository):
        self.db = role_repo


    def get_roles(self) -> List[RoleResponse]:
        try:
            print("GET ALL ROLE AT SERVICE")
            roles = self.db.get_all_roles()
            # Convert SQLAlchemy models to RoleResponse objects
            return [RoleResponse.from_orm(role) for role in roles]
        except Exception as e:
            print("ERROR GET ALL ROLE AT SERVICE")
            raise HTTPException(status_code=500, detail="ERROR GET ALL ROLE AT SERVICE: " + str(e))


    def get_role_by_name(self, name: RoleType) -> RoleResponse:
        try:
            print("GET ROLE AT SERVICE")
            role = self.db.get_role_by_name(name)
            # Convert SQLAlchemy model to RoleResponse object
            return RoleResponse.from_orm(role)
        except Exception as e:
            print("ERROR GET ROLE AT SERVICE")
            raise HTTPException(status_code=404, detail="ROLE NOT FOUND: " + str(e))


    def create_new_role(self, role: RoleRequest) -> RoleResponse:
        try:
            print("CREATE NEW ROLE AT SERVICE")
            role_new = Role(role_name=role.role_name)
            created_role = self.db.create_role(role_new)
            # Convert SQLAlchemy model to RoleResponse object
            return RoleResponse.from_orm(created_role)
        except Exception as e:
            print("ERROR CREATE NEW ROLE AT SERVICE:", str(e))
            raise HTTPException(status_code=400, detail=f"ERROR CREATE NEW ROLE AT SERVICE: {(str(e))}")