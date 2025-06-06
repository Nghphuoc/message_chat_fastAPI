from fastapi import Depends
from sqlalchemy.orm import Session

from dbconfig.config import get_db
from repository.UserRepository import UserRepository
from service.UserService import UserService


# user service
def user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)