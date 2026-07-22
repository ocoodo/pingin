from typing import Annotated

from fastapi import Depends, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repo import UserRepo
from app.chats.repo import ChatRepo
from app.auth.repo import SessionRepo
from app.messages.repo import MessageRepo

from app.users.service import UserService
from app.chats.service import ChatService
from app.auth.service import AuthService
from app.messages.service import MessageService

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


def get_chat_repo(session: DbSession) -> ChatRepo:
    return ChatRepo(session)


def get_session_repo(session: DbSession) -> SessionRepo:
    return SessionRepo(session)


def get_message_repo(session: DbSession) -> MessageRepo:
    return MessageRepo(session)


GetUserRepo = Annotated[UserRepo, Depends(get_user_repo)]
GetChatRepo = Annotated[ChatRepo, Depends(get_chat_repo)]
GetSessionRepo = Annotated[SessionRepo, Depends(get_session_repo)]
GetMessageRepo = Annotated[MessageRepo, Depends(get_message_repo)]


def get_user_service(repo: GetUserRepo) -> UserService:
    return UserService(repo)


def get_chat_service(user_repo: GetUserRepo, chat_repo: GetChatRepo) -> ChatService:
    return ChatService(user_repo, chat_repo)


def get_auth_service(user_repo: GetUserRepo, session_repo: GetSessionRepo) -> AuthService:
    return AuthService(user_repo, session_repo)


def get_message_service(chat_repo: GetChatRepo, message_repo: GetMessageRepo) -> MessageService:
    return MessageService(chat_repo, message_repo)    


GetChatService = Annotated[ChatService, Depends(get_chat_service)]
GetUserService = Annotated[UserService, Depends(get_user_service)]
GetAuthService = Annotated[AuthService, Depends(get_auth_service)]
GetMessageService = Annotated[MessageService, Depends(get_message_service)]
