from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from app.auth.models import Session


class SessionRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(
        self,
        session_id: str,
        account_id: int,
        expires_at: datetime
    ) -> Session:
        session = Session(
            session_id=session_id,
            account_id=account_id,
            expires_at=expires_at
        )
        self.session.add(session)
        await self.session.commit()
        return session
    
    async def get_by_id(
        self, session_id: str
    ) -> Session:
        session = await self.session.execute(
            select(Session)
            .options(joinedload(Session.account))
            .where(Session.session_id == session_id)
        )
        return session.scalar_one_or_none()
    
