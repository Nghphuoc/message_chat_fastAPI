from datetime import datetime

from fastapi import HTTPException

from model import UserStatus
from model.Role import RoleType
from model.User import Users
from model.schema import UserRequest, UserResponse
from repository import UserRepository
from service import RoleService, StatusService
from passlib.context import CryptContext


# encoder = CryptContext(schemes=["bcrypt"], deprecated="auto")

encoder = CryptContext(schemes=["argon2"], deprecated="auto")

class UserService:

    def __init__(self, repo : UserRepository, role: RoleService, status: StatusService):
        self.db = repo
        self.role = role
        self.status = status


    def get_user(self) -> list[UserResponse]:
        try:
            print("GET ALL FROM TABLE TB_USERS AT USER SERVICE")
            users = self.db.get_all_users()
            # Convert each SQLAlchemy model to UserResponse
            return [UserResponse.from_orm(user) for user in users]
        except Exception as e:
            print("ERROR GET ALL FROM TABLE TB_USERS AT USER SERVICE: " + str(e))
            raise Exception("ERROR GET ALL FROM TABLE TB_USERS AT USER SERVICE: " + str(e))


    def get_user_by_id(self, user_id: str) -> UserResponse:
        try:
            print("GET DETAIL FROM TABLE TB_USERS AT USER SERVICE")
            user_data = self.db.get_user_by_id(user_id)
            return UserResponse.from_orm(user_data)
        except Exception as e:
            print("ERROR GET DETAIL FROM TABLE TB_USERS AT USER SERVICE: " + str(e))
            raise Exception("ERROR GET DETAIL FROM TABLE TB_USERS AT USER SERVICE: " + str(e))


    # delete by set column
    def delete_user_by_column(self, user_id: str) -> bool:
        try:
            print("DELETE USER AT USER SERVICE")
            delete_user = self.db.get_user_by_id(user_id)
            delete_user.flagDelete = True
            return True
        except Exception as e:
            print("Error DELETE USER AT USER SERVICE: ", str(e))
            raise Exception("Error DELETE USER AT USER SERVICE: "+ str(e))


    # delete from database (for ADMIN role)
    def delete_user(self, user_id: str) -> UserResponse:
        try:
            print("DELETE USER AT USER SERVICE")
            self.db.delete_user_by_id(user_id)
            return UserResponse.from_orm(self.db.delete_user_by_id(user_id))
        except Exception as e:
            print("Error DELETE USER AT USER SERVICE: ", str(e))
            raise Exception("Error DELETE USER AT USER SERVICE: "+ str(e))


    def update_user(self ,user_id: str, user: UserRequest) -> UserResponse:
       try:
           old_user = self.db.get_user_by_id(user_id)
           if old_user is None:
               raise "Error cannot found user"

           # step 5 check phone duplication
           if old_user.phone == user.phone:
               old_user.phone = user.phone
           else:
               self.check_duplicate_phone(user.phone)
               old_user.phone = user.phone
           # update if user.password not None
           if user.password is not None:
               old_user.password = user.password

           old_user.img_url = user.img_url
           old_user.display_name = user.display_name
           old_user.flagDelete = user.flagDelete
           return self.db.create_user_(old_user)
       except Exception as e:
           print("Error UPDATE USER AT USER SERVICE: ", str(e))
           raise Exception("Error UPDATE USER AT USER SERVICE: "+str(e))


    def get_user_by_email(self, email: str) -> UserResponse:
        try:
            print("GET USER AT USER SERVICE")
            user_data = self.db.get_user_by_email(email)
            print("User data:", user_data)
            return UserResponse.from_orm(user_data)
        except Exception as e:
            print("Error GET USER AT USER SERVICE: ", str(e))
            raise Exception("Error GET USER AT USER SERVICE: "+ str(e))


    def for_got_password(self, email: str, password: str, new_password: str) -> UserResponse:
        encrypted_password = encoder.encrypt(password)
        encrypted_new_password = encoder.encrypt(new_password)
        try:
            print("FOR GOT PASSWORD AT USER SERVICE")
            user_data = self.db.get_user_by_email(email)
            if not encoder.verify(user_data.password, encrypted_password):
                raise HTTPException(status_code=404, detail="Incorrect password")
            user_data.password = encrypted_new_password
            return self.db.create_user_(user_data)
        except Exception as e:
            print("Error FOR GOT PASSWORD AT USER SERVICE: ", str(e))
            raise Exception("Error FOR GOT PASSWORD AT USER SERVICE: "+ str(e))


    def add_user(self, user: UserRequest) -> UserResponse:
        #step 4: validate param
        self.validate_user(user)
        try:
            # step 1: Resolve role
            role_id = self._resolve_user_role(user)
            #step 2: Build user data
            user_data = self._build_user_data(user, role_id)

            print("CREATE USER AT USER SERVICE")
            created_user = self.db.create_user_(user_data)
            #step 3: create status
            self._create_user_status(created_user.user_id)

            return created_user
        except Exception as e:
            print("Error CREATE USER AT USER SERVICE: ", str(e))
            raise Exception("Error CREATE USER AT USER SERVICE: " + str(e))


    #step 1 Resolve role
    def _resolve_user_role(self, user: UserRequest) -> str:
        if not user.role_id:
            role = self.role.get_role_by_role_name(RoleType.MODERATOR)
            return role.role_id
        else:
            return user.role_id


    #step 2 Build user data
    def _build_user_data(self, user: UserRequest, role_id: str) -> Users:
        password_hash = encoder.hash(user.password)
        return Users(
            username=user.username,
            password=password_hash,
            email=user.email,
            phone=user.phone,
            img_url=user.img_url,
            display_name=user.display_name,
            created_at=user.created_at,
            role_id=role_id,
            flagDelete=user.flagDelete,
        )


    #step 3 create status
    def _create_user_status(self, user_id: str):
        try:
            status = UserStatus(
                is_online=False,
                last_seen=datetime.now(),
                user_id=user_id,
            )
            self.status.insert_status(status)
        except Exception as e:
            print("ERROR CREATE USER STATUS: " + str(e))
            raise Exception("ERROR CREATE USER STATUS: " + str(e))


    # step 4: check all param user info
    def validate_user(self, user: UserRequest):
        #step 5: check phone
        self.check_duplicate_phone(user.phone)
        if self.db.get_user_by_email(user.email):
            print("EMAIL ALREADY IN TABLE TB_USERS")
            raise Exception("EMAIL ALREADY IN TABLE TB_USERS")


    # step 5: check param phone
    def check_duplicate_phone(self, phone: str):
        if self.db.get_user_by_phone(phone):
            print("Error PHONE ALREADY IN TABLE TB_USERS")
            raise Exception("Error PHONE ALREADY IN TABLE TB_USERS")


