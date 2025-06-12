from fastapi import Depends
from sqlalchemy.orm import Session

from dbconfig.config import get_db
from model.schema import UserStatusResponse
from repository.RoleRepository import RoleRepository
from repository.StatusRepository import StatusRepository
from repository.UserRepository import UserRepository
from service.RoleService import RoleService
from service.StatusService import StatusService
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


def user_status_service(db: Session = Depends(get_db)):
    repo = StatusRepository(db)
    return StatusService(repo)