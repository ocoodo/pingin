from app.server.repository import ServerRepo
from app.server.schemas import ServerOut

from app.exceptions import ForbiddenError

class ServerService:
    def __init__(self, repo: ServerRepo):
        self.repo = repo
    
    async def require_owner(self, account_id: int, server_id: int):
        member = await self.repo.get_member(account_id=account_id, server_id=server_id)
        if not member or member.role != 'owner':
            raise ForbiddenError
    
    async def require_admin(self, account_id: int, server_id: int):
        member = await self.repo.get_member(account_id=account_id, server_id=server_id)
        if not member or member.role not in ('admin', 'owner'):
            raise ForbiddenError
    
    async def new_server(
        self, name: str, owner_id: int
    ) -> ServerOut:
        server = await self.repo.add(name)
        await self.repo.add_member(server_id=server.id, account_id=owner_id, role='owner')
        return ServerOut(
            id=server.id,
            name=server.name,
            created_at=server.created_at
        )