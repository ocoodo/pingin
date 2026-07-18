from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str


class NewUser(BaseModel):
    username: str
    password: str