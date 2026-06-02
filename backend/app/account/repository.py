from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.account.models import Account


class AccountRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(
        self,
        username: str,
        email: str,
        password_hash: str
    ) -> Account:
        account = Account(
            username=username,
            email=email,
            password_hash=password_hash
        )
        self.session.add(account)
        await self.session.commit()
        return account
    
    async def get_by_email(
        self, email: str
    ) -> Optional[Account]:
        account = await self.session.execute(
            select(Account)
            .where(Account.email == email)
        )
        return account.scalar_one_or_none()
    
