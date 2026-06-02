from fastapi import APIRouter, HTTPException

from app.channel.schemas import NewChannel
from app.dependencies import CurrentAccount, GetServerService, GetChannelService
from app.exceptions import ForbiddenError

router = APIRouter(prefix='/channels')


@router.post('/')
async def new_channel(
    account: CurrentAccount,
    channel_data: NewChannel,
    server_service: GetServerService,
    channel_service: GetChannelService
):
    try:
        await server_service.require_admin(
            server_id=channel_data.server_id,
            account_id=account.id
        )
    except ForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You dont have enough permissions"
        )
    channel = await channel_service.new_channel(
        name=channel_data.name, 
        server_id=channel_data.server_id
    )
    return channel