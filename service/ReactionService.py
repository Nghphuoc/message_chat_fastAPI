from typing import List
from fastapi import HTTPException
from model import Reaction
from model.schema import ReactionRequest, ReactionResponse
from repository import ReactionRepository

""" 
@author: <PhuocHN>
@version: <1.12>
@function_id: none
"""

class ReactionService:

    def __init__(self, repo: ReactionRepository):
        self.db = repo

    """
    create or update a reaction
    @param: reaction : ReactionRequest
    @return: ReactionResponse
    """
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
                    print("UPDATE REACTION: " + update.emoji + " REACTION: " + reaction.emoji)
                    update.emoji = reaction.emoji
                    update.created_at = reaction.created_at
                    data = self.db.insert_reaction(update)
                    return ReactionResponse.from_orm(data)
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

    """
    get list reaction from message
    @param: message_id : str
    @return: ReactionResponse
    """
    def get_reactions_by_message_id(self, message_id: str) -> List[ReactionResponse]:
        try:
            print("GET REACTIONS BY MESSAGE ID AT ReactionService")
            data = self.db.get_reaction_by_message_id(message_id)
            if not data:
                return []  # hoặc raise 404 nếu muốn
            return [ReactionResponse.from_orm(item) for item in data]
        except Exception as e:
            print("ERROR GET REACTIONS BY MESSAGE ID AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message ": e})

    """
    delete a reaction from message
    @param: reaction_id : str
    @return: True
    """
    def delete_reaction(self, reaction_id: str, user_id: str):
        try:
            print("DELETE REACTION AT ReactionService")
            data = self.db.remove_reaction(reaction_id, user_id)
            return True
        except Exception as e:
            print("ERROR DELETE REACTION AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message ": e})


    """
    get a reaction from user sent to message
    @param: message_id : str
    @param: user_id : str
    @return: ReactionResponse
    """
    def get_reaction_of_user(self, message_id: str, user_id: str)-> ReactionResponse:
        try:
            print("GET REACTION OF USER AT ReactionService")
            reaction = self.db.get_reaction_by_message_id_and_user_id(message_id, user_id)
            return reaction
        except Exception as e:
            print("ERROR GET REACTION OF USER AT ReactionService: " + str(e))
            raise HTTPException(status_code=500, detail={"message": e})