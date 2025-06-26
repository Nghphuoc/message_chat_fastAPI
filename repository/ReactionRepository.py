from fastapi import HTTPException
from sqlalchemy.orm import Session

from model import Reaction


class ReactionRepository:

    def __init__(self, session: Session):
        self.db = session


    def insert_reaction(self, reaction: Reaction):
        try:
            self.db.add(reaction)
            self.db.commit()
            self.db.refresh(reaction)
            return reaction
        except Exception as e:
            raise Exception("ERROR INSERT REACTION AT ReactionRepository: ", e)


    def remove_reaction(self, reaction_id: str):
        try:
            reaction = self.db.query(Reaction).filter(Reaction.reaction_id == reaction_id).first()
            if not reaction:
                raise HTTPException(status_code=404, detail="Reaction not found")
            self.db.delete(reaction)
            self.db.commit()
        except Exception as e:
            raise Exception("ERROR REMOVE REACTION AT ReactionRepository: ", e)


    # get icon by message_id
    def get_reaction_by_message_id(self, message_id: str):
        try:
            results = self.db.query(Reaction).filter(Reaction.message_id == message_id).all()
            return results  # luôn trả list, dù rỗng hay không
        except Exception as e:
            raise Exception("ERROR GET REACTION AT ReactionRepository: " + str(e))


    def get_reaction_by_message_id_and_user_id(self, message_id: str, user_id: str):
        try:
            return (self.db.query(Reaction)
                    .filter(Reaction.message_id == message_id)
                    .filter(Reaction.user_id == user_id).one_or_none())
        except Exception as e:
            print("ERROR GET REACTION AT ReactionRepository: ", e)
            raise Exception("ERROR GET REACTION AT ReactionRepository: ", e)