from typing import Optional

from fastapi import APIRouter, Path, Query, HTTPException

from app.message.schemas import NewMessage
from app.dependencies import CurrentAccount, GetChannelService, GetMessageService
from app.exceptions import NotFoundError, ForbiddenError


router = APIRouter()


@router.post(
    '/channels/{channel_id}/messages/',
    status_code=201
)
async def send_message(
    message_data: NewMessage,
    account: CurrentAccount,
    channel_service: GetChannelService,
    message_service: GetMessageService,
    channel_id: int = Path()
):
    try:
        await channel_service.require_member(
            channel_id=channel_id, account_id=account.id
        )
    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )
    except ForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You are not member"
        )
    
    await message_service.send_message(
        channel_id=channel_id, 
        sender_id=account.id, 
        text=message_data.text
    )
    return {
        "detail": "Message sended"
    }


@router.get('/channels/{channel_id}/messages/')
async def message_history(
    account: CurrentAccount,
    channel_service: GetChannelService,
    message_service: GetMessageService,
    channel_id: int = Path(),
    before: Optional[int] = Query(None)
):
    try:
        await channel_service.require_member(
            channel_id=channel_id, account_id=account.id
        )
    except NotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )
    except ForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You are not member"
        )
    
    history = await message_service.get_history(
        channel_id=channel_id,
        before=before
    )
    return history
