from fastapi import HTTPException

from model import UserStatus
from model.schema import UserStatusResponse
from repository.StatusRepository import StatusRepository


class StatusService:

    def __init__(self, repo: StatusRepository):
        self.db = repo


    def update_status(self, user_id: str, is_online: bool) -> UserStatusResponse:
        try:
            print("UPDATE STATUS AT SATUS SERVICE")
            # call repo
            user_status = self.db.update_user_status(user_id, is_online)
            return user_status
        except Exception as e:
            print("ERROR CANNOT UPDATE STATUS AT STATUS SERVICE: " + str(e))
            raise HTTPException(status_code=400, detail=f"ERROR CANNOT UPDATE STATUS AT STATUS SERVICE: {(str(e))}")


    def insert_status(self, status: UserStatus):
        try:
            print("INSERT STATUS AT SATUS SERVICE")
            # call repo
            self.db.create_status(status)
        except Exception as e:
            print("ERROR CANNOT INSERT STATUS AT STATUS SERVICE: " + str(e))
            raise HTTPException(status_code=400, detail=f"ERROR CANNOT INSERT STATUS AT STATUS SERVICE: " + str(e))


    def get_status_by_user(self, user_id: str) -> UserStatusResponse:
        try:
            print("GET STATUS AT SATUS SERVICE")
            data = self.db.get_status_by_user_id(user_id)
            return UserStatusResponse.from_orm(data)
        except Exception as e:
            print("ERROR CANNOT GET STATUS AT STATUS SERVICE: " + str(e))
            raise HTTPException(status_code=404, detail=f"ERROR CANNOT GET STATUS AT STATUS SERVICE: " + str(e))
