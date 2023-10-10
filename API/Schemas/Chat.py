from pydantic import BaseModel


class ChatBase(BaseModel):
    offer_id: int
    creator_id: int
    time_opened: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    class Config:
        orm_mode = True