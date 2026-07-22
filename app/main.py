from fastapi import FastAPI, Depends

from app.users.router import router as user_router
from app.chats.router import router as chat_router
from app.auth.router import router as auth_router
from app.messages.router import router as message_router


app = FastAPI()


app.include_router(user_router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(message_router)
