from fastapi import FastAPI, Depends

from app.users.router import router as user_router


app = FastAPI()


app.include_router(user_router)