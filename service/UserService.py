from model.User import Users
from model.schema import UserRequest, UserResponse
from repository import UserRepository


class UserService:

    def __init__(self, repo : UserRepository):
        self.db = repo


    def get_user(self) -> list[UserResponse]:
        try:
            users = self.db.get_all_users()
            # Convert each SQLAlchemy model to UserResponse
            return [UserResponse.from_orm(user) for user in users]
        except Exception as e:
            raise e


    def add_user(self, user: UserRequest) -> UserResponse:
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
            )
            # find role by user.role_id

            created_user = self.db.create_user_(user_data)
            # Convert SQLAlchemy model to UserResponse
            return created_user
        except Exception as e:
            raise e