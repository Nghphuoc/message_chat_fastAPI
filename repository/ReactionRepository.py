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
            self.db.query(Reaction).filter(Reaction.id == reaction_id).delete()
            self.db.commit()
            self.db.refresh(Reaction)
            return True
        except Exception as e:
            raise Exception("ERROR REMOVE REACTION AT ReactionRepository: ", e)


    # get icon by message_id
    def get_reaction_by_message_id(self, message_id: str):
        try:
            return self.db.query(Reaction).filter(Reaction.message_id == message_id).all()
        except Exception as e:
            raise Exception("ERROR GET REACTION AT ReactionRepository: ", e)

