from sqlalchemy.orm import Session
from model.User import Users


class UserRepository:
    def __init__(self, session: Session):
        self.db = session


    def create_user_(self, user: Users):
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e


    def get_all_users(self):
        try:
            return self.db.query(Users).all()
        except Exception as e:
            raise e


    def get_user_by_email(self, email: str):
        try:
            return self.db.query(Users).filter(Users.email == email).first()
        except Exception as e:
            raise "Error Getting User by Email: " + str(e)


    def get_user_by_phone(self, phone: str):
        try:
            return self.db.query(Users).filter(Users.phone == phone).first()
        except Exception as e:
            raise "Error Getting User by Email: " + str(e)
