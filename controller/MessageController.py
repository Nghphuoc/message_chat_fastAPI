from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from depends.dependecy import message_service
from model.schema import MessageResponse, MessageRequest
from service import MessageService

router = APIRouter = APIRouter(prefix="/api/message", tags=["message"])


@router.post("/create", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageRequest ,service: MessageService = Depends(message_service)):
    try:
        return service.insert_message(message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})


@router.get("/all", response_model=List[MessageResponse], status_code=status.HTTP_200_OK)
async def get_all_messages(service: MessageService = Depends(message_service)):
    try:
        return service.get_message()
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e)})



