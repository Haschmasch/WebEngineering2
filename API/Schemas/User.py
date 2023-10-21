"""
Schemas for the communication over the api.
Contains schemas for users.
"""

import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    phone_number: str


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    time_created: datetime.datetime | None = None

    class Config:
        from_attributes = True
