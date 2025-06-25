from fastapi import HTTPException

from model import UserStatus
from model.schema import UserStatusResponse
from repository.StatusRepository import StatusRepository

"""
@author <PhuocHN>
@version <1.12>
@function_id none
"""

class StatusService:

    def __init__(self, repo: StatusRepository):
        self.db = repo

    """
    update status ( online or offline )
    @param: user_id : str
    @param: is_online : bool
    @return: UserStatusResponse 
    """
    def update_status(self, user_id: str, is_online: bool) -> UserStatusResponse:
        try:
            print("UPDATE STATUS AT SATUS SERVICE")
            # call repo
            user_status = self.db.update_user_status(user_id, is_online)
            return user_status
        except Exception as e:
            print("ERROR CANNOT UPDATE STATUS AT STATUS SERVICE: " + str(e))
            raise HTTPException(status_code=400, detail={"message": e})

    """
    create status ( online or offline )
    @:param status : UserStatus
    @return:  
    """
    def insert_status(self, status: UserStatus):
        try:
            print("INSERT STATUS AT SATUS SERVICE")
            # call repo
            self.db.create_status(status)
        except Exception as e:
            print("ERROR CANNOT INSERT STATUS AT STATUS SERVICE: " + str(e))
            raise HTTPException(status_code=400, detail={"message": e})

    """
    get status of user
    @param: user_id : str
    @return: UserStatusResponse 
    """
    def get_status_by_user(self, user_id: str) -> UserStatusResponse:
        try:
            print("GET STATUS AT SATUS SERVICE")
            data = self.db.get_status_by_user_id(user_id)
            return UserStatusResponse.from_orm(data)
        except Exception as e:
            print("ERROR CANNOT GET STATUS AT STATUS SERVICE: " + str(e))
            raise HTTPException(status_code=404, detail={"message": e})
