from fastapi import APIRouter, HTTPException

from app.chats.schemas import GetDirect
from app.deps import GetCurrentUser, GetChatService
from app.exceptions import NotFoundError


router = APIRouter()


@router.post('/chats/direct')
async def direct_chat(
    data: GetDirect, 
    user: GetCurrentUser,
    chat_service: GetChatService
):
    try:
        chat = await chat_service.get_direct_chat(user.id, data.user_id)
        return chat
    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

