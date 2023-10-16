import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    phone_number: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str | None = None
    name: str | None = None
    password: str


class User(UserBase):
    id: int
    time_created: datetime.datetime | None = None
    class Config:
        from_attributes = True


