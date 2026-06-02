from datetime import datetime

from pydantic import BaseModel, EmailStr


class NewSession(BaseModel):
    email: EmailStr
    password: str


class SessionOut(BaseModel):
    account_id: int
    session_id: str