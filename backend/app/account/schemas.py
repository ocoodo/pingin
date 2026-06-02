from pydantic import BaseModel, EmailStr


class NewAccount(BaseModel):
    username: str
    email: EmailStr
    password: str


class AccountOut(BaseModel):
    id: int
    username: str
    email: str
