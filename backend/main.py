import uvicorn
from fastapi import FastAPI

from app.account.router import router as account_router
from app.channel.router import router as channel_router
from app.message.router import router as message_router
from app.server.router import router as server_router
from app.auth.router import router as auth_router


app = FastAPI()


app.include_router(account_router)
app.include_router(channel_router)
app.include_router(message_router)
app.include_router(server_router)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run(app)