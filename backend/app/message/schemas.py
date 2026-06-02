from pydantic import BaseModel


class NewMessage(BaseModel):
    text: str


class MessageOut(BaseModel):
    id: int
    sender_id: int
    channel_id: int
    text: str
