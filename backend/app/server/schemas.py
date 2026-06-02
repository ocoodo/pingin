from datetime import datetime

from pydantic import BaseModel


class NewServer(BaseModel):
    name: str


class ServerOut(BaseModel):
    id: int
    name: str
    created_at: datetime
