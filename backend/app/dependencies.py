from __future__ import annotations

from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Cookie, HTTPException

from app.account.repository import AccountRepo
from app.channel.repository import ChannelRepo
from app.message.repository import MessageRepo
from app.server.repository import ServerRepo
from app.auth.repository import SessionRepo

from app.account.service import AccountService
from app.channel.service import ChannelService
from app.message.service import MessageService
from app.server.service import ServerService
from app.auth.service import AuthService

from app.account.schemas import AccountOut
from app.exceptions import InvalidSessionError
from app.database import get_session


async def get_current_account(
    auth_service: GetAuthService,
    session_id: str = Cookie(None)
) -> AccountOut:
    try:
        account = await auth_service.verify_session(session_id)
    except InvalidSessionError:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )
    return account


def get_account_repo(db_session: DbSession) -> AccountRepo:
    return AccountRepo(db_session)


def get_session_repo(db_session: DbSession) -> SessionRepo:
    return SessionRepo(db_session)


def get_server_repo(db_session: DbSession) -> ServerRepo:
    return ServerRepo(db_session)


def get_channel_repo(db_session: DbSession) -> ChannelRepo:
    return ChannelRepo(db_session)


def get_message_repo(db_session: DbSession) -> MessageRepo:
    return MessageRepo(db_session)


def get_account_service(account_repo: GetAccountRepo) -> AccountService:
    return AccountService(account_repo)


def get_server_service(server_repo: GetServerRepo) -> ServerService:
    return ServerService(server_repo)


def get_message_service(message_repo: GetMessageRepo) -> MessageService:
    return MessageService(message_repo)


def get_channel_service(
    server_repo: GetServerRepo,
    channel_repo: GetChannelRepo
) -> ChannelService:
    return ChannelService(
        server_repo=server_repo,
        channel_repo=channel_repo
    )


def get_auth_service(
    account_repo: GetAccountRepo,
    session_repo: GetSessionRepo
) -> AuthService:
    return AuthService(
        account_repo=account_repo,
        session_repo=session_repo
    )


GetAccountRepo = Annotated[AccountRepo, Depends(get_account_repo)]
GetSessionRepo = Annotated[SessionRepo, Depends(get_session_repo)]
GetMessageRepo = Annotated[MessageRepo, Depends(get_message_repo)]
GetServerRepo = Annotated[ServerRepo, Depends(get_server_repo)]
GetChannelRepo = Annotated[ChannelRepo, Depends(get_channel_repo)]


GetAccountService = Annotated[AccountService, Depends(get_account_service)]
GetAuthService = Annotated[AuthService, Depends(get_auth_service)]
GetServerService = Annotated[ServerService, Depends(get_server_service)]
GetChannelService = Annotated[ChannelService, Depends(get_channel_service)]
GetMessageService = Annotated[MessageService, Depends(get_message_service)]


DbSession = Annotated[AsyncSession, Depends(get_session)]
CurrentAccount = Annotated[AccountOut, Depends(get_current_account)]
