from typing import List

from fastapi import HTTPException

from model import Reaction
from model.schema import ReactionRequest, ReactionResponse
from repository import ReactionRepository


class ReactionService:

    def __init__(self, repo: ReactionRepository):
        self.db = repo


    def create_reaction_and_update(self, reaction: ReactionRequest) -> ReactionResponse :
        try:
            # step 1: find reaction of message and user
            update = self.get_reaction_of_user(reaction.message_id, reaction.user_id)
            # step 1.1: check find reaction
            if update:
                # step 1.2: if emoji same to same -> not update
                if update.emoji == reaction.emoji:
                    return ReactionResponse.from_orm(update)
                else:
                    # step 1.3: call service update reaction
                    update.emoji = reaction.emoji
                    update.created_at = reaction.created_at
                    return self.db.insert_reaction(update)
            else:
                # step 2: create new reaction
                print("CREATE REACTION AT ReactionService")
                data = Reaction(user_id=reaction.user_id,
                                message_id=reaction.message_id,
                                emoji=reaction.emoji,
                                created_at= reaction.created_at)

                data_reaction = self.db.insert_reaction(data)
                return ReactionResponse.from_orm(data_reaction)
        except Exception as e:
            print("ERROR CREATE REACTION AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message ": e})


    def get_reactions_by_message_id(self, message_id: str) -> List[ReactionResponse]:
        try:
            print("GET REACTIONS BY MESSAGE ID AT ReactionService")
            data = self.db.get_reaction_by_message_id(message_id)
            return [ReactionResponse.from_orm(item) for item in data]
        except Exception as e:
            print("ERROR GET REACTIONS BY MESSAGE ID AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message ": e})


    def delete_reaction(self, reaction_id: str):
        try:
            print("DELETE REACTION AT ReactionService")
            data = self.db.remove_reaction(reaction_id)
            return True
        except Exception as e:
            print("ERROR DELETE REACTION AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message ": e})


    # step 1: find reaction of message and user
    def get_reaction_of_user(self, message_id: str, user_id: str)-> ReactionResponse:
        try:
            print("GET REACTION OF USER AT ReactionService")
            reaction = self.db.get_reaction_by_message_id_and_user_id(message_id, user_id)
            return reaction
        except Exception as e:
            print("ERROR GET REACTION OF USER AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e})