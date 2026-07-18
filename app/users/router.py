from fastapi import APIRouter, HTTPException

from app.users.schemas import NewUser
from app.exceptions import AlreadyInUseError
from app.deps import GetUserService, GetCurrentUser


router = APIRouter()


@router.post(
    '/users/',
    status_code=201
)
async def new_user(data: NewUser, user_service: GetUserService):
    try:
        user = await user_service.new_user(data.username, data.password)
        return user
    except AlreadyInUseError:
        raise HTTPException(
            status_code=409,
            detail="Username already in use"
        )


@router.get('/users/me')
def get_me(user: GetCurrentUser):
    return user