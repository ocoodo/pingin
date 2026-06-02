import secrets
from datetime import datetime, timedelta, timezone

from app.account.repository import AccountRepo
from app.account.schemas import AccountOut
from app.auth.repository import SessionRepo
from app.auth.schemas import SessionOut
from app.exceptions import InvalidCredentialsError, InvalidSessionError
from app.security import verify_password
from app.settings import settings


class AuthService:
    def __init__(
        self,
        account_repo: AccountRepo,
        session_repo: SessionRepo
    ):
        self.account_repo = account_repo
        self.session_repo = session_repo
    
    async def login(
        self, email: str, password: str
    ) -> SessionOut:
        account = await self.account_repo.get_by_email(email)
        if not account or not verify_password(password, account.password_hash):
            raise InvalidCredentialsError
        
        session_id = secrets.token_hex(32)
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.session_expire_days
        )
        session = await self.session_repo.add(
            session_id=session_id,
            account_id=account.id,
            expires_at=expires_at
        )
        return SessionOut(
            account_id=session.account_id,
            session_id=session.session_id
        )
    
    async def verify_session(
        self, session_id: str
    ) -> AccountOut:
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise InvalidSessionError
        
        session_expires = session.expires_at.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if now > session_expires:
            raise InvalidSessionError
        
        account = session.account
        return AccountOut(
            id=account.id,
            username=account.username,
            email=account.email
        )
    
    