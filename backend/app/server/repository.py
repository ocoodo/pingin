from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.server.models import Server, ServerMember


class ServerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(
        self, name: str
    ) -> Server:
        server = Server(
            name=name
        )
        self.session.add(server)
        await self.session.commit()
        return server
    
    async def add_member(
        self, server_id: int, account_id: int, role: str
    ) -> ServerMember:
        member = ServerMember(
            account_id=account_id,
            server_id=server_id,
            role=role
        )
        self.session.add(member)
        await self.session.commit()
    
    async def get_member(
         self, server_id: int, account_id: int
    ) -> Optional[ServerMember]:
        member = await self.session.execute(
            select(ServerMember)
            .where(
                ServerMember.server_id == server_id,
                ServerMember.account_id == account_id
            )
        )
        return member.scalar_one_or_none()
