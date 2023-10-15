import datetime

from pydantic import BaseModel


class ChatBase(BaseModel):
    offer_id: int
    creator_id: int
    time_opened: datetime.datetime | None = None


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int

    class Config:
        from_attributes = True
