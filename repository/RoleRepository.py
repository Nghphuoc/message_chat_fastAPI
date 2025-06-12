from sqlalchemy.orm import Session

from model import Role
from model.Role import RoleType


class RoleRepository:

    def __init__(self, session: Session):
        self.db = session


    def get_all_roles(self):
        return self.db.query(Role).all()


    def create_role(self, role: Role):
        try:
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        except Exception as e:
            self.db.rollback()
            raise Exception("Error Creating the Role: " + str(e))


    def get_role_by_name(self, name: RoleType):
        try:
            return self.db.query(Role).filter(Role.role_name == name).one()
        except Exception as e:
            raise Exception("Error Getting The Role: " + str(e))


    def update_role(self, role_id: str, new_role: Role):
        try:
            self.db.query(Role).filter(Role.role_id == role_id).update(new_role)
            self.db.commit()
            self.db.refresh(new_role)
            return new_role
        except Exception as e:
            self.db.rollback()
            raise Exception("Error Updating the Role: " + str(e))