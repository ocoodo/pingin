from typing import Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from app.auth.models import Session


class SessionRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, id: str, user_id: int, expires_at: datetime) -> Session:
        new_session = Session(
            id=id,
            user_id=user_id,
            expires_at=expires_at
        )
        self.session.add(new_session)
        await self.session.commit()
        return new_session
    
    async def get_by_id(self, id: str) -> Optional[Session]:
        session = await self.session.execute(
            select(Session)
            .options(joinedload(Session.user))
            .where(Session.id == id)
        )
        return session.scalar_one_or_none()
        