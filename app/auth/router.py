from fastapi import APIRouter, Response, HTTPException

from app.auth.schemas import Credentials
from app.exceptions import InvalidCredentialsError
from app.deps import GetAuthService
from app.settings import settings


router = APIRouter()


@router.post(
    '/auth/session',
    status_code=201
)
async def login(credentials: Credentials, response: Response, auth_service: GetAuthService):
    try:
        session = await auth_service.login(credentials.username, credentials.password)
        response.set_cookie(
            key="session_id",
            value=session.session_id,
            httponly=True,
            samesite="lax",
            max_age=(settings.session_expire_days * 24 * 3600)
        )
        return {'ok': True}
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )