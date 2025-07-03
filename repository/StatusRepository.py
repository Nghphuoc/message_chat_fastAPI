from datetime import datetime

from sqlalchemy.orm import Session

from model import UserStatus


class StatusRepository:

    def __init__(self, session: Session):
        self.db = session


    def get_all_status(self):
        try:
            self.db.query(UserStatus).all()
            self.db.commit()
            self.db.refresh(UserStatus)
        except Exception as e:
            self.db.rollback()
            print("Error getting status" + str(e))
            raise Exception("Error getting status" + str(e))


    def create_status(self, status: UserStatus):
        try:
            self.db.add(status)
            self.db.commit()
            self.db.refresh(status)
        except Exception as e:
            self.db.rollback()
            print("Error creating status" + str(e))
            raise Exception("Error creating status" + str(e))


    def get_status_by_id(self, status_id: str):
        try:
            self.db.query(UserStatus).filter(UserStatus.status_id == status_id).one()
        except Exception as e:
            self.db.rollback()
            print("Error getting status" + str(e))
            raise Exception("Error getting status" + str(e))


    def get_status_by_user_id(self, user_id: str):
        try:
            status = self.db.query(UserStatus).filter(UserStatus.user_id == user_id).first()
            if not status:
                raise Exception("Status not found")
            return status
        except Exception as e:
            self.db.rollback()
            print("Error getting status: " + str(e))
            raise


    def update_user_status(self, user_id: str, is_online: bool):
        try:
            status = self.db.query(UserStatus).filter_by(user_id=user_id).first()

            # step 1 create if don't have status
            if not status:
                status = UserStatus(
                    user_id=user_id,
                    is_online=is_online,
                    last_seen=datetime.utcnow()
                )
                self.db.add(status)
            else:
                # step 2 open status online
                status.is_online = is_online
                status.last_seen = datetime.utcnow()

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("Error updating status" + str(e))
            raise Exception("Error updating status" + str(e))