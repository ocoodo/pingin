from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.messages.schemas import NewMessage
from app.exceptions import NotFoundError
from app.deps import GetMessageService


router = APIRouter()


@router.post(
    '/chats/{chat_id}/messages',
    status_code=201
)
async def new_message(
    chat_id: Annotated[int, Path(ge=1)],
    content: NewMessage,
    message_service: GetMessageService
):
    try:
        await message_service.send(chat_id, content.text)
        return {"ok": True}
    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )


@router.get('/chats/{chat_id}/messages')
async def get_messages(chat_id):
    pass
