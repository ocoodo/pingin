from pydantic import BaseModel


class SessionOut(BaseModel):
    session_id: str
    user_id: int


class Credentials(BaseModel):
    username: str
    password: str