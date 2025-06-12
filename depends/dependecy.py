from fastapi import Depends
from sqlalchemy.orm import Session

from dbconfig.config import get_db
from repository.RoleRepository import RoleRepository
from repository.UserRepository import UserRepository
from service.RoleService import RoleService
from service.UserService import UserService


# user service
def user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

# role service
def role_service(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    return RoleService(repo)