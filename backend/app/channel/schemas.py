from datetime import datetime

from pydantic import BaseModel


class NewChannel(BaseModel):
    name: str
    server_id: int


class ChannelOut(BaseModel):
    id: int
    name: str
    server_id: int
    created_at: datetime
