from sqlalchemy.exc import SQLAlchemyError
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

    def remove_reaction(self, reaction_id: str, user_id: str):
        try:
            reaction = (
                self.db.query(Reaction)
                .filter(Reaction.reaction_id == reaction_id, Reaction.user_id == user_id)
                .first()
            )
            if not reaction:
                print("NOT AUTHORIZE TO DELETE EMOJI")
                raise Exception("REACTION NOT FOUND")
            else:
                self.db.delete(reaction)
                self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"ERROR REMOVE REACTION AT ReactionRepository: {str(e)}")


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