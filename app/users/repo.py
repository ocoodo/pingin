from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, username: str, password_hash: str) -> User:
        new_user = User(
            username=username,
            password_hash=password_hash
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user
    
    async def get_by_username(self, username: str) -> Optional[User]:
        user = await self.session.execute(
            select(User)
            .where(User.username == username)
        )
        return user.scalar_one_or_none()
    
    async def get_by_id(self, id: int) -> Optional[User]:
        user = await self.session.execute(
            select(User)
            .where(User.id == id)
        )
        return user.scalar_one_or_none()