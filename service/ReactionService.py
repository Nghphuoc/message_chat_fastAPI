from typing import List

from fastapi import HTTPException

from model import Reaction
from model.schema import ReactionRequest, ReactionResponse
from repository import ReactionRepository


class ReactionService:

    def __init__(self, repo: ReactionRepository):
        self.db = repo


    def create_reaction(self, reaction: ReactionRequest) -> ReactionResponse :
        try:
            print("CREATE REACTION AT ReactionService")
            data = Reaction(user_id=reaction.user_id,
                            message_id=reaction.message_id,
                            emoji=reaction.emoji,
                            created_at= reaction.created_at)

            data_reaction = self.db.insert_reaction(data)
            return ReactionResponse.from_orm(data_reaction)
        except Exception as e:
            print("ERROR CREATE REACTION AT ReactionService: " + str(e))
            raise HTTPException(status_code=500,
                                detail="ERROR CREATE REACTION AT ReactionService: " + str(e))


    def get_reactions_by_message_id(self, message_id: str) -> List[ReactionResponse]:
        try:
            print("GET REACTIONS BY MESSAGE ID AT ReactionService")
            data = self.db.get_reaction_by_message_id(message_id)
            return [ReactionResponse.from_orm(item) for item in data]
        except Exception as e:
            print("ERROR GET REACTIONS BY MESSAGE ID AT ReactionService: " + str(e))
            raise HTTPException(status_code=500,
                                detail="ERROR GET REACTIONS BY MESSAGE ID AT ReactionService: " + str(e))


    def delete_reaction(self, reaction_id: str):
        try:
            print("DELETE REACTION AT ReactionService")
            data = self.db.remove_reaction(reaction_id)
            return True
        except Exception as e:
            print("ERROR DELETE REACTION AT ReactionService: " + str(e))
            raise HTTPException(status_code=500,
                                detail="ERROR DELETE REACTION AT ReactionService: " + str(e))