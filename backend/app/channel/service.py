from app.channel.repository import ChannelRepo
from app.server.repository import ServerRepo
from app.channel.schemas import ChannelOut
from app.exceptions import NotFoundError, ForbiddenError


class ChannelService:
    def __init__(
        self,
        server_repo: ServerRepo,
        channel_repo: ChannelRepo
    ):
        self.server_repo = server_repo
        self.channel_repo = channel_repo
    
    async def require_member(self, channel_id: int, account_id: int):
        channel = await self.channel_repo.get_by_id(channel_id)
        if not channel:
            raise NotFoundError
        
        member = await self.server_repo.get_member(
            server_id=channel.server_id, account_id=account_id
        )
        if not member:
            raise ForbiddenError
    
    async def new_channel(
        self, name: str, server_id: int
    ) -> ChannelOut:
        channel = await self.channel_repo.add(name=name, server_id=server_id)
        return ChannelOut(
            id=channel.id,
            name=channel.name,
            server_id=channel.server_id,
            created_at=channel.created_at
        )