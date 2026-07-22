from pydantic import BaseModel


class NewMessage(BaseModel):
    text: str


class MessageOut(BaseModel):
    id: int
    chat_id: int
    text: str
