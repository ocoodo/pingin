from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.channel.models import Channel


class ChannelRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(
        self, channel_id: int
    ) -> Channel:
        channel = await self.session.execute(
            select(Channel)
            .where(Channel.id == channel_id)
        )
        return channel.scalar_one_or_none()
    
    async def add(
        self, name: str, server_id: int
    ) -> Channel:
        channel = Channel(
            name=name,
            server_id=server_id
        )
        self.session.add(channel)
        await self.session.commit()
        return channel
    