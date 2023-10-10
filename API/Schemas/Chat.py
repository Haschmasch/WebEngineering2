from pydantic import BaseModel


class ChatBase(BaseModel):
    offerid: int
    creatorid: int
    timeopened: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    class Config:
        orm_mode = True