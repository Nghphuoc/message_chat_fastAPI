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
            results = self.db.query(Reaction).filter(Reaction.message_id == message_id).all()

            if not results:
                # Không có reaction nào
                return None
            elif len(results) == 1:
                # Có đúng 1 reaction
                return results[0]
            else:
                # Có nhiều reaction
                return results

        except Exception as e:
            raise Exception("ERROR GET REACTION AT ReactionRepository: ", e)


    def get_reaction_by_message_id_and_user_id(self, message_id: str, user_id: str):
        try:
            return (self.db.query(Reaction)
                    .filter(Reaction.message_id == message_id)
                    .filter(Reaction.user_id == user_id).one_or_none())
        except Exception as e:
            print("ERROR GET REACTION AT ReactionRepository: ", e)
            raise Exception("ERROR GET REACTION AT ReactionRepository: ", e)