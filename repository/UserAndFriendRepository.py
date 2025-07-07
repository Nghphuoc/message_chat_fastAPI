from sqlalchemy.orm import Session
from sqlalchemy import case, func, literal, or_, select, and_
from sqlalchemy.orm import aliased
from model import Friendship, Users

class UserAndFriendRepository:

    def __init__(self, db: Session):
        self.db = db


    def search_users_with_status(self, current_user_id: str, keyword: str):
        FriendAlias = aliased(Friendship)

        # Subquery: lấy mối quan hệ bạn bè 2 chiều
        subquery = (
            self.db.query(
                case(
                    (FriendAlias.user_id == current_user_id, FriendAlias.friend_id),
                    else_=FriendAlias.user_id
                ).label("other_user_id"),
                FriendAlias.status.label("status")
            )
            .filter(
                or_(
                    FriendAlias.user_id == current_user_id,
                    FriendAlias.friend_id == current_user_id
                )
            )
            .subquery()
        )

        # Truy vấn chính: join user + subquery để lấy trạng thái bạn bè
        results = (
            self.db.query(
                Users.user_id,
                Users.display_name,
                Users.img_url,
                func.coalesce(subquery.c.status, "NONE").label("friendship_status")
            )
            .outerjoin(subquery, subquery.c.other_user_id == Users.user_id)
            .filter(
                and_(
                    Users.user_id != current_user_id,
                    func.lower(Users.display_name).like(f"%{keyword.lower()}%")
                )
            )

            .all()
        )

        return results
