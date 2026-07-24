from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from app.messages.schemas import NewMessage
from app.exceptions import NotFoundError, ForbiddenError
from app.deps import GetMessageService, GetCurrentUser


router = APIRouter()


@router.post(
    '/chats/{chat_id}/messages',
    status_code=201
)
async def new_message(
    chat_id: Annotated[int, Path(ge=1)],
    content: NewMessage,
    user: GetCurrentUser,
    message_service: GetMessageService,
):
    try:
        await message_service.send(chat_id, user.id, content.text)
        return {"ok": True}
    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    except ForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You are not member"
        )


@router.get('/chats/{chat_id}/messages')
async def get_messages(
    chat_id: Annotated[int, Path(ge=1)],
    user: GetCurrentUser,
    message_service: GetMessageService,
    limit: int = Query(50, ge=1, le=100),
    before: int = Query(None, ge=1)
):
    try:
        messages = await message_service.get_messages(chat_id, user.id, limit, before)
        return messages
    except ForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You are not memeber"
        )
