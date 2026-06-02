from fastapi import APIRouter, HTTPException

from app.account.schemas import NewAccount
from app.dependencies import GetAccountService, CurrentAccount
from app.exceptions import AlreadyExistsError


router = APIRouter(prefix="/accounts")


@router.post(
    "/",
    status_code=201
)
async def add_account(
    account: NewAccount,
    account_service: GetAccountService
):
    try:
        new_account = await account_service.new_account(
            username=account.username,
            email=account.email,
            password=account.password
        )
    except AlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Account with this email already exists"
        )
    return {
        "detail": f"Account {new_account.email} created"
    }


@router.get('/me')
async def me(
    account: CurrentAccount
):
    return account