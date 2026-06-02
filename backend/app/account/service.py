from app.account.repository import AccountRepo
from app.account.schemas import AccountOut
from app.security import get_password_hash
from app.exceptions import AlreadyExistsError


class AccountService:
    def __init__(self, repo: AccountRepo):
        self.repo = repo
    
    async def new_account(
        self,
        username: str,
        email: str,
        password: str
    ) -> AccountOut:
        exists = await self.repo.get_by_email(email)
        if exists:
            raise AlreadyExistsError
        
        password_hash = get_password_hash(password)
        account = await self.repo.add(
            username=username,
            email=email,
            password_hash=password_hash
        )
        return AccountOut(
            id=account.id,
            username=account.username,
            email=account.email
        )
        