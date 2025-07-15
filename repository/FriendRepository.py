from fastapi import HTTPException
from sqlalchemy.orm import Session
from model import Friendship
from model.Friendship import TypeStatus
from model.schema import FriendRequest


class FriendRepository:

    def __init__(self, session: Session):
        self.db = session


    def create_friend(self, friend: Friendship):
        try:
            self.db.add(friend)
            self.db.commit()
            self.db.refresh(friend)
            return friend
        except Exception as e:
            print("ERROR CREATE FRIEND AT REPO: " + str(e))
            raise Exception("ERROR CREATE FRIEND AT REPO: " + str(e))


    # find and update request friend
    def update_friend_status(self, friend: FriendRequest):
        try:
            print("UPDATE FRIEND STATUS AT FRIEND SERVICE")

            # Find the existing friendship record
            existing = self.db.query(Friendship).filter(
                Friendship.user_id == friend.user_id,
                Friendship.friend_id == friend.friend_id
            ).first()
            if not existing:
                raise HTTPException(status_code=404, detail="Friendship not found")
            # Update the status
            existing.status = friend.status
            self.db.commit()
            self.db.refresh(existing)

            return existing
        except Exception as e:
            print("ERROR UPDATE FRIEND AT FRIEND SERVICE: " + str(e))
            raise HTTPException(
                status_code=500,
                detail="ERROR UPDATE FRIEND AT FRIEND SERVICE: " + str(e)
            )


    # get all friend for user
    def get_friends_by_user_id(self, user_id: str):
        try:
            data_friend = self.db.query(Friendship).filter(
                Friendship.user_id == user_id,
                Friendship.status == TypeStatus.ACCEPTED
            ).all()
            return data_friend
        except Exception as e:
            print("ERROR GET FRIEND AT REPO: " + str(e))
            raise Exception("ERROR GET FRIEND AT REPO: " + str(e))


    # get detail user
    def get_detail_user(self, user_id: str, friend_id: str):
        try:
            data_friend = self.db.query(Friendship).filter(Friendship.user_id == user_id,
                                                           Friendship.friend_id == friend_id).one_or_none()
            return data_friend
        except Exception as e:
            print("ERROR GET FRIEND AT REPO: " + str(e))
            return None  # đừng raise nữa


    # delete duplicat user_id and friend_id
    def delete_friend_relationship(self, user_id: str, friend_id: str):
        try:
            # delete at user
            self.db.query(Friendship).filter(Friendship.user_id == user_id, friend_id == friend_id).delete()
            # delete at friend
            self.db.query(Friendship).filter(Friendship.user_id == friend_id, friend_id == user_id).delete()
            self.db.commit()
            self.db.refresh(Friendship)
            return True
        except Exception as e:
            print("ERROR DELETE FRIEND AT REPO: " + str(e))
            raise Exception("ERROR DELETE FRIEND AT REPO: " + str(e))


    def get_friend_relationship(self, user_id: str, friend_id: str):
        try:
            data = self.db.query(Friendship).filter(Friendship.user_id == user_id, Friendship.friend_id == friend_id).one()
            self.db.commit()
            self.db.refresh(data)
            return data
        except Exception as e:
            print("ERROR GET FRIEND AT REPO: " + str(e))
            raise Exception("ERROR GET FRIEND AT REPO: " + str(e))


    # get all request for user
    def get_request_add_friend(self, user_id: str):
        try:
            data_friend = self.db.query(Friendship).filter(
                Friendship.user_id == user_id
            ).all()
            return data_friend
        except Exception as e:
            print("ERROR GET FRIEND AT REPO: " + str(e))
            raise Exception("ERROR GET FRIEND AT REPO: " + str(e))
