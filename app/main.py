from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.deps import DbSession


app = FastAPI()