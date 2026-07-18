from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repo import UserRepo
from app.users.service import UserService 

from app.database import get_session


DbSession = Annotated[AsyncSession, Depends(get_session)]


def get_user_repo(session: DbSession) -> UserRepo:
    return UserRepo(session)


GetUserRepo = Annotated[UserRepo, Depends(get_user_repo)]


def get_user_service(repo: GetUserRepo) -> UserService:
    return UserService(repo)
    

GetUserService = Annotated[UserService, Depends(get_user_service)]