from model.User import Users
from model.schema import UserRequest, UserResponse
from repository import UserRepository


class UserService:

    def __init__(self, repo : UserRepository):
        self.db = repo


    def get_user(self) -> list[UserResponse]:
        try:
            print("GET ALL FROM TABLE TB_USERS AT USER SERVICE")
            users = self.db.get_all_users()
            # Convert each SQLAlchemy model to UserResponse
            return [UserResponse.from_orm(user) for user in users]
        except Exception as e:
            print("ERROR GET ALL FROM TABLE TB_USERS AT USER SERVICE: " + str(e))
            raise e


    def get_user_by_id(self, user_id: str) -> UserResponse:
        try:
            print("GET DETAIL FROM TABLE TB_USERS AT USER SERVICE")
            self.db.get_user_by_id(user_id)
            return UserResponse.from_orm(self.db.get_user_by_id(user_id))
        except Exception as e:
            print("ERROR GET DETAIL FROM TABLE TB_USERS AT USER SERVICE: " + str(e))



    def add_user(self, user: UserRequest) -> UserResponse:
        self.validate_user(user)

        try:
            user_data = Users(
                username=user.username,
                password=user.password,
                email=user.email,
                phone=user.phone,
                img_url=user.img_url,
                display_name=user.display_name,
                created_at=user.created_at,
                role_id=user.role_id,
                flagDelete= user.flagDelete,
            )
            # find role by user.role_id
            print("CREATE USER AT USER SERVICE")
            created_user = self.db.create_user_(user_data)
            # Convert SQLAlchemy model to UserResponse
            return created_user
        except Exception as e:
            print("Error CREATE USER AT USER SERVICE: ", str(e))
            raise e


    def update_user(self ,user_id: str, user: UserRequest) -> UserResponse:
       try:
           old_user = self.db.get_user_by_id(user_id)
           if old_user is None:
               raise "Error cannot found user"

           #check phone duplication
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
           raise "Error UPDATE USER AT USER SERVICE: "+str(e)


    def validate_user(self, user: UserRequest):
        self.check_duplicate_phone(user.phone)
        if self.db.get_user_by_email(user.email):
            print("EMAIL ALREADY IN TABLE TB_USERS")
            raise Exception("EMAIL ALREADY IN TABLE TB_USERS")


    def check_duplicate_phone(self, phone: str):
        if self.db.get_user_by_phone(phone):
            print("Error PHONE ALREADY IN TABLE TB_USERS")
            raise Exception("Error PHONE ALREADY IN TABLE TB_USERS")