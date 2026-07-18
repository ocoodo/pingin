from typing import Annotated

from fastapi import Depends, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repo import UserRepo
from app.auth.repo import SessionRepo
from app.users.service import UserService
from app.auth.service import AuthService 

from app.users.schemas import UserOut
from app.exceptions import InvalidSessionError
from app.database import get_session


async def get_current_user(auth_service: 'GetAuthService', session_id: str = Cookie(None)) -> UserOut:
    try:
        user = await auth_service.verify_session(session_id)
        return user
    except InvalidSessionError:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )


GetCurrentUser = Annotated[UserOut, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_session)]


def get_user_repo(session: DbSession) -> UserRepo:
    return UserRepo(session)

def get_session_repo(session: DbSession) -> SessionRepo:
    return SessionRepo(session)


GetUserRepo = Annotated[UserRepo, Depends(get_user_repo)]
GetSessionRepo = Annotated[SessionRepo, Depends(get_session_repo)]


def get_user_service(repo: GetUserRepo) -> UserService:
    return UserService(repo)

def get_auth_service(user_repo: GetUserRepo, session_repo: GetSessionRepo) -> AuthService:
    return AuthService(user_repo, session_repo)
    

GetUserService = Annotated[UserService, Depends(get_user_service)]
GetAuthService = Annotated[AuthService, Depends(get_auth_service)]