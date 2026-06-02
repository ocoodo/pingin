from fastapi import APIRouter, Response, HTTPException

from app.auth.schemas import NewSession
from app.dependencies import GetAccountService, GetAuthService
from app.exceptions import InvalidCredentialsError
from app.settings import settings


router = APIRouter(prefix="/auth")


@router.post(
    "/sessions/",
    status_code=201
)
async def new_session(
    response: Response,
    credentials: NewSession,
    auth_service: GetAuthService,
):
    try:
        session = await auth_service.login(
            email=credentials.email, 
            password=credentials.password
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    response.set_cookie(
        key="session_id",
        value=session.session_id,
        httponly=True,
        samesite="lax",
        secure=settings.https_cookies,
        max_age=settings.session_expire_days * 24 * 60 * 60
    )
    
    return {
        "detail": "Session created"
    }