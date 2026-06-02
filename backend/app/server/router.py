from fastapi import APIRouter

from app.server.schemas import NewServer
from app.dependencies import CurrentAccount, GetServerService


router = APIRouter(prefix='/servers')


@router.post('/')
async def new_server(
    account: CurrentAccount,
    server_data: NewServer,
    server_service: GetServerService
):
    server = await server_service.new_server(
        name=server_data.name,
        owner_id=account.id
    )
    return server