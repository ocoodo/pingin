from datetime import datetime, timezone, timedelta

from app.auth.schemas import SessionOut
from app.users.schemas import UserOut
from app.auth.repo import SessionRepo
from app.users.repo import UserRepo
from app.exceptions import InvalidCredentialsError, InvalidSessionError
from app.utils import verify_password, generate_session_id
from app.settings import settings

class AuthService:
    def __init__(self, user_repo: UserRepo, session_repo: SessionRepo):
        self.user_repo = user_repo
        self.session_repo = session_repo
    
    async def login(self, username: str, password: str) -> SessionOut:
        user = await self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        
        session_id = generate_session_id()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.session_expire_days)
        session = await self.session_repo.add(session_id, user.id, expires_at)
        return SessionOut(
            session_id=session.id,
            user_id=session.user_id
        )
    
    async def verify_session(self, session_id: str) -> UserOut:
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise InvalidSessionError
        
        now = datetime.now(timezone.utc)
        if session.expires_at < now:
            raise InvalidSessionError
        
        return UserOut(
            id=session.user.id,
            username=session.user.username
        )
        