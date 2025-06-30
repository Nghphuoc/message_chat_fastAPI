from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from depends.dependecy import reaction_service
from model.schema import ReactionResponse, ReactionRequest
from service import ReactionService

router = APIRouter(prefix="/api/reaction", tags=["reaction"])


@router.get("/detail/{message_id}", response_model=list[ReactionResponse], status_code=status.HTTP_200_OK)
async def get_detail(message_id: str, service: ReactionService = Depends(reaction_service)):
    try:
        return service.get_reactions_by_message_id(message_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.post("/create", response_model=ReactionResponse, status_code=status.HTTP_201_CREATED)
async def create_and_update(reaction: ReactionRequest, service: ReactionService = Depends(reaction_service)):
    try:
        return service.create_reaction_and_update(reaction)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})


@router.delete("/delete/{reaction_id}/{user_id}", status_code=status.HTTP_200_OK)
async def delete(reaction_id: str, user_id: str, service: ReactionService = Depends(reaction_service)):
    try:
        if service.delete_reaction(reaction_id, user_id):
            return {"message": "Reaction deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Reaction not found"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": str(e)})
